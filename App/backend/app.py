from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
import logging
import os
from real_chatbot import detect_company, query_llm, extract_sql_and_notes, execute_sql  # Import your chatbot functions
from real_chatbot_rag import load_faiss_index, query_llm_groq
from classifier import classify_question  # Import the classification logic
from dotenv import load_dotenv
import oracledb

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ SQLite DB Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Retrieve database configuration
db_config = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "dsn": os.getenv("DB_DSN"),
        "wallet_location": os.getenv("DB_WALLET_LOCATION"),
    }

# ✅ Chat Model
class ChatSession(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.String(50))

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(10))  # 'user' or 'bot'
    message = db.Column(db.Text)
    session_id = db.Column(db.String(50), db.ForeignKey('chat_session.id'))

# ✅ Initialize the DB
with app.app_context():
    db.create_all()

# ✅ Route to Save Chat Message
@app.route('/save_chat', methods=['POST'])
def save_chat():
    data = request.get_json()
    session_id = data['session_id']
    user_id = data['user_id']
    sender = data['sender']
    message = data['message']

    # Convert list or nested list responses to a string
    if isinstance(message, list):
        message = str(message[0][0]) if message and isinstance(message[0], list) else str(message)

    chat_session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
    if not chat_session:
        return jsonify({"status": "Error", "message": "Invalid session or unauthorized"}), 403

    chat_message = Chat(sender=sender, message=message, session_id=session_id)
    db.session.add(chat_message)
    db.session.commit()

    return jsonify({"status": "Message saved!"}), 201


# ✅ Route to Create New Chat Session
@app.route('/new_session', methods=['POST'])
def new_session():
    data = request.get_json()
    user_id = data['user_id']

    new_session_id = str(uuid.uuid4())
    new_chat_session = ChatSession(id=new_session_id, title=f"Chat {new_session_id[:8]}", user_id=user_id)
    db.session.add(new_chat_session)
    db.session.commit()

    return jsonify({"session_id": new_session_id, "title": new_chat_session.title}), 201

# ✅ Route to Get Chat Sessions for a Specific User
@app.route('/get_sessions/<user_id>', methods=['GET'])
def get_sessions(user_id):
    sessions = ChatSession.query.filter_by(user_id=user_id).all()
    session_data = [{"id": session.id, "title": session.title} for session in sessions]
    return jsonify(session_data)

# ✅ Route to Get Chat Messages for a Session
@app.route('/get_chats/<session_id>', methods=['GET'])
def get_chats(session_id):
    chats = Chat.query.filter_by(session_id=session_id).all()
    chat_history = [{'sender': chat.sender, 'message': chat.message} for chat in chats]
    return jsonify(chat_history)

# ✅ Route to Get All Chat Sessions
@app.route('/get_all_sessions/<user_id>', methods=['GET'])
def get_all_sessions(user_id):
    sessions = ChatSession.query.filter_by(user_id=user_id).all()
    session_list = [{'session_id': session.id, 'title': session.title} for session in sessions]
    return jsonify(session_list)

# ✅ Route to Delete a Chat Session
@app.route('/delete_chat/<session_id>', methods=['DELETE'])
def delete_chat(session_id):
    try:
        Chat.query.filter_by(session_id=session_id).delete()
        ChatSession.query.filter_by(id=session_id).delete()
        db.session.commit()
        return jsonify({"status": "Chat deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "Error deleting chat", "error": str(e)}), 500

# ✅ Route to Cleanup Empty Sessions
@app.route('/cleanup_empty_sessions', methods=['DELETE'])
def cleanup_empty_sessions():
    try:
        active_sessions = db.session.query(Chat.session_id).distinct().all()
        active_session_ids = [session[0] for session in active_sessions]
        empty_sessions = ChatSession.query.filter(~ChatSession.id.in_(active_session_ids)).all()

        for session in empty_sessions:
            db.session.delete(session)

        db.session.commit()
        return jsonify({"status": "Empty chat sessions cleaned up!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "Error during cleanup", "error": str(e)}), 500

# ✅ Route to Get a Specific Chat Session
@app.route('/get_chat/<session_id>', methods=['GET'])
def get_chat(session_id):
    try:
        chat_session = ChatSession.query.filter_by(id=session_id).first()
        if chat_session:
            messages = Chat.query.filter_by(session_id=session_id).all()
            message_list = [{'sender': msg.sender, 'message': msg.message} for msg in messages]
            return jsonify({"messages": message_list}), 200
        else:
            return jsonify({"status": "Error", "message": "Session not found"}), 404
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)}), 500

# ✅ Route to Query Real Chatbot
@app.route('/query_chatbot', methods=['POST'])
def query_chatbot():
    data = request.get_json()
    print("Received data:", data)  # 🔍 Debug log

    user_question = data.get("question")
    session_id = data.get("session_id")
    user_id = data.get("user_id")
    selected_company = data.get("selected_company")  # ✅ Matching key name

    print("User Question:", user_question)
    print("Session ID:", session_id)
    print("User ID:", user_id)
    print("Selected Company:", selected_company)

    # Validation
    if not user_question or not session_id or not user_id or not selected_company:
        return jsonify({"error": "Invalid request data - Missing required fields"}), 400

    classification = classify_question(user_question)

    if classification == 'numerical':
        return handle_numerical_query(user_question, session_id, user_id, selected_company)
    else:
        return handle_contextual_query(user_question, selected_company)

def get_ddl_prefix_from_db(company_name):
    """Fetch DDL prefix from the Oracle database mapping table."""
    connection = oracledb.connect(
            user=db_config["user"],
            password=db_config["password"],
            dsn=db_config["dsn"],
            config_dir=db_config["wallet_location"],
            wallet_location=db_config["wallet_location"],
            wallet_password=db_config["password"]
            )
    cursor = connection.cursor()

    query = "SELECT DDL_PREFIX FROM COMPANY_MAPPING WHERE LOWER(COMPANY_NAME) = LOWER(:company_name)"
    cursor.execute(query, {"company_name": company_name})
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result[0] if result else None

def get_company_names_from_db():
    """Fetch distinct company names from the COMPANY_MAPPING table."""
    connection = oracledb.connect(
        user=db_config["user"],
        password=db_config["password"],
        dsn=db_config["dsn"],
        config_dir=db_config["wallet_location"],
        wallet_location=db_config["wallet_location"],
        wallet_password=db_config["password"]
    )
    cursor = connection.cursor()
    query = "SELECT DISTINCT UPPER(COMPANY_NAME) FROM COMPANY_MAPPING"
    cursor.execute(query)
    
    companies = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    
    return companies

@app.route('/api/companies', methods=['GET'])
def fetch_companies():
    """API Endpoint to get company names"""
    return jsonify(get_company_names_from_db())

def handle_numerical_query(user_question, session_id, user_id, selected_company):
    # ✅ Validate if a company is selected
    if not selected_company:
        return jsonify({"error": "No company selected for numerical query"}), 400
    ddl_directory = "Oracle_DDLs"
    model_name = "llama-3.3-70b-versatile"

    # Retrieve API keys as a list
    api_keys = os.getenv("API_KEYS").split(",")

    # ddl_prefix = detect_company(selected_company)
    ddl_prefix = get_ddl_prefix_from_db(selected_company)

    if ddl_prefix:
        ddl_file_path = os.path.join(ddl_directory, f"{ddl_prefix}_ddl.sql")
    else:
        return jsonify({"error": "Company not recognized"}), 404

    if not os.path.exists(ddl_file_path):
        return jsonify({"error": "DDL not found for the specified company"}), 404

    with open(ddl_file_path, "r", encoding="utf-8") as ddl_file:
        ddl_content = ddl_file.read().strip()

    api_key = api_keys[0]  # Cycle through if needed
    llm_output, llm_time = query_llm(user_question, ddl_content, model_name, api_key)

    if not llm_output:
        return jsonify({"error": "Failed to generate a response from LLM."}), 500

    sql_query, notes = extract_sql_and_notes(llm_output)
    if sql_query:
        print(f"Generated SQL Query: {sql_query}")
        results, columns, exec_time, error_msg = execute_sql(sql_query, db_config)
        if results:
            formatted_results = str(results[0][0]) if results else "No data found"
            return jsonify({"response": formatted_results}), 200
        else:
            return jsonify({"error": error_msg}), 500
    else:
        return jsonify({"error": "Failed to extract SQL query from LLM response."}), 500
    
# ✅ Handle Contextual (RAG-based) Queries
def handle_contextual_query(user_question, selected_company):
    vector_store = load_faiss_index()
    if vector_store is None:
        return jsonify({"error": "Vector store not available. Please run the embedding process first."}), 500
    
    final_query = f"[Company: {selected_company}] {user_question}"

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    response, relevant_docs = query_llm_groq(final_query, retriever)

    if isinstance(response, str) and response.startswith("❌"):
        return jsonify({"error": response}), 500

    sources = [{"source": doc["source"], "snippet": doc["text"][:200]} for doc in relevant_docs]
    return jsonify({
        "response": response,
        "sources": sources
    }), 200



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
