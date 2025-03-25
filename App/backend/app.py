#----------------------------------------Imports----------------------------------------
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
import logging
import os
from real_chatbot import query_llm, extract_sql_and_notes, execute_sql  # Import chatbot functions
from real_chatbot_rag import query_llm_groq, load_vector_store
from dotenv import load_dotenv
import oracledb
from groq import Groq  # ✅ Required for Groq API
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

#----------------------------------------Environment Setup----------------------------------------
# Load environment variables from .env file
load_dotenv()

#----------------------------------------Flask App Initialization----------------------------------------
app = Flask(__name__)
CORS(app)

# Initialize thread-local storage for database sessions
db_lock = threading.Lock()

#----------------------------------------Groq client----------------------------------------------------#
api_keys = os.getenv("API_KEYS")
if not api_keys:
    print("We are currently unable to process this request. Please try again later.")

api_keys = api_keys.split(",")
api_key = api_keys[2]

try:
    client = Groq(api_key=api_key)
except Exception:
    print("We are currently experiencing technical difficulties. Please try again later.")

#----------------------------------------Database Setup----------------------------------------
# ✅ SQLite DB Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 20,
    'max_overflow': 0,
    'pool_pre_ping': True
}
db = SQLAlchemy(app)

# Retrieve database configuration
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dsn": os.getenv("DB_DSN"),
    "wallet_location": os.getenv("DB_WALLET_LOCATION"),
}

#----------------------------------------Database Models----------------------------------------
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

#----------------------------------------Routes----------------------------------------

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

    with db_lock:
        try:
            chat_session = ChatSession.query.filter_by(id=session_id, user_id=user_id).first()
            if not chat_session:
                return jsonify({"status": "Error", "message": "Invalid session or unauthorized"}), 403

            chat_message = Chat(sender=sender, message=message, session_id=session_id)
            db.session.add(chat_message)
            db.session.commit()
            return jsonify({"status": "Message saved!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "Error", "message": str(e)}), 500

# ✅ Route to Create New Chat Session
@app.route('/new_session', methods=['POST'])
def new_session():
    data = request.get_json()
    user_id = data['user_id']

    new_session_id = str(uuid.uuid4())
    with db_lock:
        try:
            new_chat_session = ChatSession(id=new_session_id, title=f"Chat {new_session_id[:8]}", user_id=user_id)
            db.session.add(new_chat_session)
            db.session.commit()
            return jsonify({"session_id": new_session_id, "title": new_chat_session.title}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "Error", "message": str(e)}), 500

# ✅ Route to Get Chat Sessions for a Specific User
@app.route('/get_sessions/<user_id>', methods=['GET'])
def get_sessions(user_id):
    with db_lock:
        try:
            sessions = ChatSession.query.filter_by(user_id=user_id).all()
            session_data = [{"id": session.id, "title": session.title} for session in sessions]
            return jsonify(session_data)
        except Exception as e:
            return jsonify({"status": "Error", "message": str(e)}), 500

# ✅ Route to Get Chat Messages for a Session
@app.route('/get_chats/<session_id>', methods=['GET'])
def get_chats(session_id):
    with db_lock:
        try:
            chats = Chat.query.filter_by(session_id=session_id).all()
            chat_history = [{'sender': chat.sender, 'message': chat.message} for chat in chats]
            return jsonify(chat_history)
        except Exception as e:
            return jsonify({"status": "Error", "message": str(e)}), 500

# ✅ Route to Get All Chat Sessions
@app.route('/get_all_sessions/<user_id>', methods=['GET'])
def get_all_sessions(user_id):
    with db_lock:
        try:
            sessions = ChatSession.query.filter_by(user_id=user_id).all()
            session_list = [{'session_id': session.id, 'title': session.title} for session in sessions]
            return jsonify(session_list)
        except Exception as e:
            return jsonify({"status": "Error", "message": str(e)}), 500

# ✅ Route to Delete a Chat Session
@app.route('/delete_chat/<session_id>', methods=['DELETE'])
def delete_chat(session_id):
    with db_lock:
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
    with db_lock:
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
    with db_lock:
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

#----------------------------------------Updated Chatbot Query Route----------------------------------------
@app.route('/query_chatbot', methods=['POST'])
def query_chatbot():
    data = request.get_json()
    print("Received data:", data)

    user_question = data.get("question")
    session_id = data.get("session_id")
    user_id = data.get("user_id")
    selected_company = data.get("selected_company")

    if not user_question or not session_id or not user_id or not selected_company:
        return jsonify({"error": "Invalid request data - Missing required fields"}), 400

    # Create a copy of the app context for thread safety
    app_ctx = app.app_context()
    
    def run_in_context(fn, *args):
        with app_ctx:
            return fn(*args)

    # Use ThreadPoolExecutor to run both queries concurrently
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_num = executor.submit(run_in_context, handle_numerical_query, user_question, selected_company)
        future_ctx = executor.submit(run_in_context, handle_contextual_query, user_question, selected_company)

        # Wait for both futures to complete
        numerical_data, numerical_status = future_num.result()
        contextual_data, contextual_status = future_ctx.result()

    # Process results
    numerical_text = numerical_data.get('response') if numerical_status == 200 else str(numerical_data.get('error'))
    contextual_text = contextual_data.get('response') if contextual_status == 200 else str(contextual_data.get('error'))

    print("SQL Output:", numerical_text)
    print("RAG Output:", contextual_text)
    
    # Run summarizer
    summarized_response = summarize_responses(user_question, numerical_text, contextual_text)

    return jsonify({"response": summarized_response}), 200


@app.route('/api/companies', methods=['GET'])
def fetch_companies():
    """API Endpoint to get company names"""
    return jsonify(get_company_names_from_db())
    
#----------------------------------------Utility Functions----------------------------------------

#----------------------------------------Summarization Function----------------------------------------
def summarize_responses(user_question, numerical_response, contextual_response):
    model_name = "mistral-saba-24b"
    max_retries = 3
    prompt = f"""
    You are an AI assistant that prioritizes the numerical response from a SQL Database to answer financial questions, supported by a contextual RAG response. Your job is to decide the correct answer, then FORMAT the output correctly based on the user's question.

    ### Decision Rule:
    - Prioritize the SQL numerical response if it directly answers the user's question.
    - Use the contextual response only if SQL data is insufficient or irrelevant.
    - Always use the **user question** to understand if the expected answer is a **percentage**, **monetary amount**, or **count**.

    ### Formatting Guidelines:
    - If the user asks about **percentage change, growth, or decrease**, format the number as a percentage (e.g.,'1.24 becomes `-1.24%`, `12.5 becomes 12.5%`).
    - If the user asks about **revenue, profit, income, shareholder equity**, or any **monetary value**, format as currency:
        - Use `$` sign  (e.g., `143 becomes $143`, `22.7 becomes $22.7`)
        - Add commas for readability (e.g., `$25,500`)
        - NEVER add in decimals or round the original numerical answer.
    - If the user asks for a **count** (like number of employees, units, or quarters), return the raw number with commas if large (`5,000`).
    - Do not repeat the question. No explanations.

    ###Inputs:
    User Question: {user_question}
    Numerical Response (SQL): {numerical_response}
    Contextual Response (RAG): {contextual_response}

    If you used the numerical response, always end with:
    "All monetary values are in millions."
"""

    for attempt in range(max_retries):
        try:
            llm_response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": prompt}],
                max_tokens=300,
                temperature=0.3
            )

            formatted_response = llm_response.choices[0].message.content.strip()

            if not formatted_response or formatted_response.lower().startswith("error"):
                raise ValueError("Invalid response received from LLM.")

            return formatted_response
        except Exception as e:
            error_message = str(e).lower()

            if "503" in error_message or "service unavailable" in error_message:
                if attempt == max_retries - 1:
                    return "We are currently experiencing high demand. Please try again later."
                time.sleep((attempt + 1) * 2)
                continue

            if "rate limit" in error_message or "too many requests" in error_message:
                if attempt == max_retries - 1:
                    return "We are currently handling a high number of requests. Please try again in a few minutes."
                time.sleep((attempt + 1) * 2)
                continue

            if "unauthorized" in error_message or "invalid api key" in error_message:
                return "We are currently unable to process this request. Please try again later."

            if attempt == max_retries - 1:
                return "We are experiencing technical difficulties. Please try again later."

            time.sleep((attempt + 1) * 2)

    return "We are experiencing technical difficulties. Please try again later."

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
def handle_numerical_query(user_question, selected_company):
    try:
        if not selected_company:
            return {"error": "No company selected for numerical query"}, 400
        
        ddl_directory = "Oracle_DDLs"
        model_name = "llama-3.3-70b-versatile"
        api_keys = os.getenv("API_KEYS").split(",")
        ddl_prefix = get_ddl_prefix_from_db(selected_company)

        if ddl_prefix:
            ddl_file_path = os.path.join(ddl_directory, f"{ddl_prefix}_ddl.sql")
        else:
            return {"error": "Company not recognized"}, 404

        if not os.path.exists(ddl_file_path):
            return {"error": "DDL not found for the specified company"}, 404

        with open(ddl_file_path, "r", encoding="utf-8") as ddl_file:
            ddl_content = ddl_file.read().strip()

        api_key = api_keys[1]
        llm_output, llm_time = query_llm(user_question, ddl_content, model_name, api_key)

        if not llm_output:
            return {"error": "Failed to generate a response from LLM."}, 500

        sql_query, notes = extract_sql_and_notes(llm_output)
        if sql_query:
            print(f"Generated SQL Query: {sql_query}")
            write_operation_patterns = [
                r"\b(?:insert|update|delete|drop|create|rename|replace|modify|insertMany|updateMany|bulkWrite)\b",
                r"\$set\b", 
                r"\$push\b", 
                r"\$addToSet\b",  
                r"\$pull\b"  
            ]
            for pattern in write_operation_patterns:
                if re.search(pattern, sql_query, re.IGNORECASE):
                    return {"error": "Failed to run SQL query due to security concerns."}, 500

            results, columns, exec_time, error_msg = execute_sql(sql_query, db_config)
            if results:
                formatted_results = str(results[0][0]) if results else "No data found"
                return {"response": formatted_results}, 200
            else:
                return {"error": error_msg}, 500
        else:
            return {"error": "Failed to extract SQL query from LLM response."}, 500
    except Exception as e:
        return {"error": str(e)}, 500
    

# ✅ Handle Contextual (RAG-based) Queries
def handle_contextual_query(user_question, selected_company):
    """Handle contextual queries using MongoDB Atlas Vector Search."""
    try:
        
        vector_store = load_vector_store()
        if vector_store is None:
            return {"error": "Vector store not available. Please check MongoDB connection."}, 500
        
        final_query = f"[Company: {selected_company}] {user_question}"
        response, relevant_docs = query_llm_groq(final_query, vector_store, selected_company)

        if isinstance(response, str) and response.startswith("❌"):
            return {"error": response}, 500

        sources = [{"source": doc["source"], "snippet": doc["text"][:200]} for doc in relevant_docs]
        return {
            "response": response,
            "sources": sources
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500

#----------------------------------------Main Execution----------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)