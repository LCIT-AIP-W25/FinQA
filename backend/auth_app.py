from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from dotenv import load_dotenv
import os
import secrets
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

#  Load environment variables
load_dotenv()

AUTH_API_URL = "https://finqa-auth-app-ac1o.onrender.com";
Frontend_URL = "https://finqaai.netlify.app"

#  Initialize Flask App
auth_app = Flask(__name__)
CORS(auth_app)
bcrypt = Bcrypt(auth_app)

#  SQLite Configuration
auth_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URI')
# 'sqlite:///users.db'
auth_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Configure SendGrid SMTP for Email Sending
auth_app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.sendgrid.net')
auth_app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
auth_app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
auth_app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'apikey')
auth_app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
auth_app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

#  Initialize Database & Mail
db = SQLAlchemy(auth_app)
mail = Mail(auth_app)

#  User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)  #  No longer unique
    email = db.Column(db.String(120), unique=True, nullable=False)  #  Email must be unique
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)  #  Store if the email is verified
    verification_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


#  Initialize Database
with auth_app.app_context():
    db.create_all()

def send_verification_email(email, verification_url):
    try:
        sendgrid_api_key = os.getenv('MAIL_PASSWORD')  # This is the SendGrid API Key
        sender_email = os.getenv('MAIL_DEFAULT_SENDER')

        if not sendgrid_api_key or not sender_email:
            print("❌ SendGrid API Key or Sender Email is missing.")
            return False

        email_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h2>Verify Your Email Address</h2>
            <p>Click the button below to verify your email:</p>
            <a href="{verification_url}" style="background-color: #28a745; padding: 10px 15px; color: white; text-decoration: none; border-radius: 5px;">
                Verify Email
            </a>
            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p><a href="{verification_url}">{verification_url}</a></p>
        </body>
        </html>
        """

        message = Mail(
            from_email=sender_email,
            to_emails=email,
            subject="Verify Your Email Address",
            html_content=email_content
        )

        sg = SendGridAPIClient(sendgrid_api_key)
        response = sg.send(message)

        if response.status_code in [200, 202]:
            print(f"✅ Verification email sent to {email}")
            return True
        else:
            print(f"❌ SendGrid failed with status code {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False


# 🔐 Signup Route (with Email Verification)
@auth_app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        if existing_user.is_verified:
            return jsonify({'status': 'error', 'message': 'Email already registered and verified. Please log in.'}), 400
        else:
            #  Allow re-signup if email is not verified (resend verification)
            verification_token = secrets.token_hex(16)
            existing_user.verification_token = verification_token
            db.session.commit()
            verification_url = f"{AUTH_API_URL}/verify_email/{verification_token}"
            send_verification_email(email, verification_url)  #  Send new verification email
            return jsonify({'status': 'success', 'message': 'Verification email resent. Please check your inbox and spam folder.'})

    #  Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    verification_token = secrets.token_hex(16)

    new_user = User(username=username, email=email, password=hashed_password, verification_token=verification_token)
    db.session.add(new_user)
    db.session.commit()

    #  Send verification email
    verification_url = f"{AUTH_API_URL}/verify_email/{verification_token}"
    send_verification_email(email, verification_url)

    return jsonify({'status': 'success', 'message': 'Verification email sent! Please check your inbox and spam folder.'})

#  Email Verification Route
@auth_app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return """
        <html>
            <body style="text-align: center; font-family: Arial, sans-serif; margin-top: 50px;">
                <h2 style="color: red;">❌ Verification Failed</h2>
                <p>The verification link is invalid or has expired.</p>
                <p>Please try signing up again.</p>
            </body>
        </html>
        """, 400

    if user.is_verified:
        return """
        <html>
            <body style="text-align: center; font-family: Arial, sans-serif; margin-top: 50px;">
                <h2 style="color: #28a745;">✅ Email Already Verified!</h2>
                <p>You can log in now.</p>
                <a href="{frontend_url}/login">Go to Login</a>
            </body>
        </html>
        """.format(frontend_url=Frontend_URL), 400

    #  Mark email as verified
    user.is_verified = True
    user.verification_token = None  #  Clear token after successful verification
    db.session.commit()

    return """
    <html>
        <head>
            <meta http-equiv="refresh" content="3;url={frontend_url}/login">
        </head>
        <body style="text-align: center; font-family: Arial, sans-serif; margin-top: 50px;">
            <h2 style="color: #28a745;">✅ Email Verified Successfully!</h2>
            <p>You will be redirected to the login page shortly.</p>
            <p>If not redirected, <a href="{frontend_url}/login">click here</a>.</p>
        </body>
    </html>
    """.format(frontend_url=Frontend_URL), 200


# 🔐 Login Route
@auth_app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'User does not exist.'}), 401

    if not user.is_verified:
        return jsonify({'status': 'error', 'message': 'Email not verified. Please check your email for verification link.'}), 401

    if bcrypt.check_password_hash(user.password, password):
        return jsonify({'status': 'success', 'message': 'Login successful.', 'user_id': user.id, 'username': user.username})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials.'}), 401


# 🔑 Forget Password Route

@auth_app.route('/forget_password', methods=['POST'])
def forget_password():
    data = request.get_json()

    print(f"📩 Received Forget Password Request: {data}")

    if not data or 'email' not in data:
        print("❌ No email provided!")
        return jsonify({'status': 'error', 'message': 'Email is required.'}), 400

    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        print(f"❌ Email {email} not found in the database!")
        return jsonify({'status': 'error', 'message': 'Email not registered.'}), 404

    #  Generate Secure Reset Token
    reset_token = secrets.token_hex(16)
    expiry_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

    user.reset_token = reset_token
    user.reset_token_expiry = expiry_time
    db.session.commit()

    reset_url = f"{Frontend_URL}/reset_password/{reset_token}"

    #  HTML Email Template with Clickable Button
    email_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; background-color: #f8f9fa; padding: 20px;">
        <div style="max-width: 500px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px #ccc;">
            <h2 style="color: #2c3e50; text-align: center;">Password Reset Request</h2>
            <p>Hello <b>{user.username}</b>,</p>
            <p>You requested to reset your password. Click the button below to reset it:</p>
            
            <div style="text-align: center; margin: 20px 0;">
                <a href="{reset_url}" style="
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 12px 25px;
                    font-size: 16px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    ">
                    Reset Password
                </a>
            </div>

            <p>If the button doesn't work, copy and paste this link into your browser:</p>
            <p><a href="{reset_url}" style="word-break: break-all; color: #3498db;">{reset_url}</a></p>

            <p><b>This link will expire in 30 minutes.</b></p>

            <p>Regards,<br><b>WealthWiz Team</b></p>
        </div>
    </body>
    </html>
    """

    #  Send Email Using SendGrid Web API
    try:
        message = Mail(
            from_email=os.getenv('MAIL_DEFAULT_SENDER'),
            to_emails=user.email,
            subject="Password Reset Request",
            html_content=email_content  #  Use HTML content
        )

        sg = SendGridAPIClient(os.getenv('MAIL_PASSWORD'))
        response = sg.send(message)

        print(f"✅ Email sent successfully! Status Code: {response.status_code}")
        return jsonify({'status': 'success', 'message': 'Password reset link sent to your email.', 'reset_url': reset_url})

    except Exception as e:
        print(f"❌ Email Sending Failed: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to send email.', 'error': str(e)}), 500


# 🔑 Reset Password Route
@auth_app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    reset_token = data.get('token')
    new_password = data.get('password')

    print(f"📩 Reset Request Received: Token={reset_token}, New Password={new_password}")

    #  Validate input
    if not reset_token or not new_password:
        print("❌ Missing Token or Password!")
        return jsonify({'status': 'error', 'message': 'Token and new password are required.'}), 400

    user = User.query.filter_by(reset_token=reset_token).first()

    if not user:
        print("❌ Invalid Reset Token!")
        return jsonify({'status': 'error', 'message': 'Invalid reset token.'}), 400

    #  Ensure the token hasn't expired
    if user.reset_token_expiry and user.reset_token_expiry < datetime.datetime.utcnow():
        print("❌ Expired Reset Token!")
        return jsonify({'status': 'error', 'message': 'Reset token has expired. Request a new one.'}), 400

    #  Hash the new password before storing
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password

    #  Clear the reset token to prevent reuse
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    print("✅ Password Reset Successful!")
    return jsonify({'status': 'success', 'message': 'Password reset successful. You can now login.'})


#  Run Authentication App
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10001))  # Default to 10001 if PORT is not set
    auth_app.run(debug=False, host='0.0.0.0', port=port)
