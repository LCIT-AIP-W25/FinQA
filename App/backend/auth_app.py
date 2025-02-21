from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# ✅ Initialize Flask App
auth_app = Flask(__name__)
CORS(auth_app)
bcrypt = Bcrypt(auth_app)

# ✅ SQLite Configuration
auth_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
auth_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(auth_app)

# ✅ User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ✅ Initialize Database
with auth_app.app_context():
    db.create_all()

# 🔐 Signup Route
@auth_app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'message': 'Email already registered.'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'User registered successfully.'})

# 🔐 Login Route
@auth_app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({'status': 'success', 'message': 'Login successful.', 'user_id': user.id, 'username': user.username})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials.'}), 401

# 🔑 Forget Password Route (Reset functionality placeholder)
@auth_app.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'Email not registered.'}), 404

    # 🔥 Here you can implement email sending functionality
    return jsonify({'status': 'success', 'message': 'Password reset link sent to your email.'})

# ✅ Run Authentication App
if __name__ == '__main__':
    auth_app.run(port=5001, debug=True)
