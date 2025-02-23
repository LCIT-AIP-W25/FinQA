from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
import logging
import os
from real_chatbot import detect_company, query_llm, extract_sql_and_notes, execute_sql  # Import your chatbot functions

app = Flask(__name__)
CORS(app)

# ✅ SQLite DB Setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    user_question = data.get("question")
    session_id = data.get("session_id")
    user_id = data.get("user_id")

    if not user_question or not session_id or not user_id:
        return jsonify({"error": "Invalid request data"}), 400

    ddl_directory = r"backend\Oracle_DDLs"
    model_name = "llama-3.1-8b-instant"
    api_keys = [
        "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",
        "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",
        "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",
        "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"
    ]
    db_config = {
        "user": "ADMIN",
        "password": "Passwordtestdb@1",
        "dsn": "testdb_medium",
        "wallet_location": r"backend\Wallet_testdb"
    }

    ddl_prefix = detect_company(user_question)
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
            # Convert list-like results to a readable format
            formatted_results = str(results[0][0]) if results else "No data found"
            return jsonify({"response": formatted_results}), 200
        else:
            return jsonify({"error": error_msg}), 500
    else:
        return jsonify({"error": "Failed to extract SQL query from LLM response."}), 500


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
