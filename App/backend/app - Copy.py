from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid

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
    sender = data['sender']
    message = data['message']

    chat_message = Chat(sender=sender, message=message, session_id=session_id)
    db.session.add(chat_message)
    db.session.commit()

    return jsonify({"status": "Message saved!"}), 201


# ✅ Route to Create New Chat Session with User ID
@app.route('/new_session', methods=['POST'])
def new_session():
    data = request.get_json()
    user_id = data['user_id']  # ✅ Get user ID from request

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

# ✅ Dummy Chat Response
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    
    # ✅ Provide a static response
    bot_response = "Thank you for your question. I'll get back to you shortly."
    return jsonify({"answer": bot_response})

# ✅ Route to Get All Chat Sessions
@app.route('/get_all_sessions', methods=['GET'])
def get_all_sessions():
    sessions = Chat.query.with_entities(Chat.session_id).distinct().all()
    session_list = [{'session_id': session[0]} for session in sessions]
    return jsonify(session_list)

# ✅ Route to Delete a Chat Session
@app.route('/delete_chat/<session_id>', methods=['DELETE'])
def delete_chat(session_id):
    try:
        Chat.query.filter_by(session_id=session_id).delete()
        db.session.commit()
        return jsonify({"status": "Chat deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "Error deleting chat", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
