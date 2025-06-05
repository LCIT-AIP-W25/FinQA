#----------------------------------------Imports----------------------------------------
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import uuid
import os
from real_chatbot import query_llm, extract_sql_and_notes, execute_sql
from real_chatbot_rag import query_llm_groq, initialize_components
from dotenv import load_dotenv
import oracledb
import time
import re
from concurrent.futures import ThreadPoolExecutor
import threading
from PDFProcessing import FinancialRAGSystem
from groq_wrapper import GroqWrapper
from groq_key_manager import key_manager
import shutil
import stat
from datetime import datetime as dt
import psutil
import logging

# Configure logging once
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_memory(tag="MEMORY"):
    process = psutil.Process(os.getpid())
    mem = psutil.virtual_memory()
    rss = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    logging.info(f"[{tag}] Total: {mem.total / (1024 ** 3):.1f} GB | Used: {mem.used / (1024 ** 3):.1f} GB | Free: {mem.free / (1024 ** 3):.1f} GB")
    logging.info(f"[{tag}] Process RSS: {rss:.1f} MB | Threads: {process.num_threads()}")


#----------------------------------------Environment Setup----------------------------------------
# Load environment variables from .env file
load_dotenv()

# Initialize key manager
key_manager.initialize_keys(
    rag_keys=os.getenv("GROQ_API_KEY_RAG").split(","),
    sql_keys=os.getenv("GROQ_API_KEY_SQL").split(","),
    summarize_keys=os.getenv("GROQ_API_KEY_SUMMARIZE").split(",")
)

# ---------------------------------------DB Connect------------------------------------------------------

def get_db_connection():
    # Load credentials from environment variables (set in Render Secrets)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_dsn = os.getenv("DB_DSN")  # e.g., "my_db_alias" (must match tnsnames.ora)
    db_wallet = os.getenv("DB_WALLET_LOCATION")

    # Establish connection using the wallet
    connection = oracledb.connect(
        user=db_user,
        password=db_password,
        dsn=db_dsn,
        config_dir=db_wallet,  # Points to /opt/wallet
        wallet_location=db_wallet,
        wallet_password=db_password,  # Optional (if ewallet.p12 is used)
        retry_count=3,
        retry_delay=1
    )
    return connection

#----------------------------------------Flask App Initialization----------------------------------------
app = Flask(__name__)
log_memory("Startup")

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URI')
# 'sqlite:///chats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'max_overflow': 0,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)
db_lock = threading.Lock()

#---------------------------------------Initialize RAG components----------------------------------------
# Lazy initialization of RAG system and components
rag_system = None
components_initialized = False

@app.before_request
def ensure_components():
     global rag_system, components_initialized
     if not components_initialized:
         print("🔄 Initializing components...")
         rag_system = FinancialRAGSystem()
         if initialize_components():
             components_initialized = True
             print("✅ RAG initialized successfully")
             log_memory("RAG Initialized")
         else:
             print("❌ RAG initialization failed")
            #raise RuntimeError("RAG initialization failed")
        
@app.route('/health', methods=['GET'])
def health_check():
    status = {"timestamp": dt.utcnow().isoformat()}

    process = psutil.Process(os.getpid())
    mem = psutil.virtual_memory()
    status["memory"] = {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "used_gb": round(mem.used / (1024 ** 3), 2),
        "rss_mb": round(process.memory_info().rss / (1024 * 1024), 1),
        "threads": process.num_threads()
    }

    status["rag_initialized"] = "✅" if components_initialized else "❌"

    try:
        conn = get_db_connection()
        conn.ping()
        conn.close()
        status["oracle_db"] = "✅ Connected"
    except Exception as e:
        status["oracle_db"] = f"❌ Failed: {str(e)}"

    return jsonify(status), 200


#----------------------------------------Database Models----------------------------------------
# Chat Model
class ChatSession(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=dt.utcnow)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(10))  # 'user' or 'bot'
    message = db.Column(db.Text)
    session_id = db.Column(db.String(50), db.ForeignKey('chat_session.id'))
    created_at = db.Column(db.DateTime, default=dt.utcnow)

# Initialize the DB
with app.app_context():
    db.create_all()



#----------------------------------------Routes----------------------------------------

# Route to Save Chat Message
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

# Route to Create New Chat Session
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

# Route to Get Chat Sessions for a Specific User
@app.route('/get_sessions/<user_id>', methods=['GET'])
def get_sessions(user_id):
    with db_lock:
        try:
            sessions = ChatSession.query.filter_by(user_id=user_id).all()
            session_data = [{"id": session.id, "title": session.title} for session in sessions]
            return jsonify(session_data)
        except Exception as e:
            return jsonify({"status": "Error", "message": str(e)}), 500

# Route to Get Chat Messages for a Session
@app.route('/get_chats/<session_id>', methods=['GET'])
def get_chats(session_id):
    with db_lock:
        try:
            chats = Chat.query.filter_by(session_id=session_id).all()
            chat_history = [{'sender': chat.sender, 'message': chat.message} for chat in chats]
            return jsonify(chat_history)
        except Exception as e:
            return jsonify({"status": "Error", "message": str(e)}), 500

# Route to Get All Chat Sessions
@app.route('/get_all_sessions/<user_id>', methods=['GET'])
def get_all_sessions(user_id):
    with db_lock:
        try:
            sessions = ChatSession.query.filter_by(user_id=user_id).all()
            session_list = [{'session_id': session.id, 'title': session.title, 'created_at': session.created_at.isoformat()} for session in sessions]
            return jsonify(session_list)
        except Exception as e:
            return jsonify({"status": "Error", "message": str(e)}), 500

# Route to Delete a Chat Session
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

# Route to Cleanup Empty Sessions
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

# Route to Get a Specific Chat Session
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



# Add after your existing routes

@app.route('/api/yahoo_news', methods=['GET'])
def get_yahoo_news():
    try:
        # Using SQLAlchemy to query PostgreSQL
        sql = """
            SELECT title, link, published_date, source
            FROM yahoo_news
            ORDER BY published_date DESC
            LIMIT 10
        """
        result = db.session.execute(sql)
        news_items = [
            {
                "title": row[0],
                "link": row[1],
                "published_date": row[2].strftime("%Y-%m-%d %H:%M:%S"),
                "source": row[3]
            }
            for row in result
        ]
        return jsonify(news_items), 200
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return jsonify({"error": "Failed to fetch news"}), 500

#----------------------------------------Updated Chatbot Query Route----------------------------------------
@app.route('/query_chatbot', methods=['POST'])
def query_chatbot():
    log_memory("Before query_chatbot")
    data = request.get_json()
    user_question = data.get("question")
    session_id = data.get("session_id")
    user_id = data.get("user_id")
    selected_company = data.get("selected_company")

    if not user_question or not session_id or not user_id or not selected_company:
        return jsonify({"error": "Invalid request data - Missing required fields"}), 400

    try:
        with db_lock:
            chat_messages = Chat.query.filter_by(session_id=session_id).order_by(Chat.id).all()
            chat_history = [{'sender': msg.sender, 'message': msg.message} for msg in chat_messages]

        numerical_data, numerical_status = handle_numerical_query(user_question, selected_company, session_id)
        contextual_data, contextual_status = handle_contextual_query(user_question, selected_company, session_id)

        numerical_text = numerical_data.get('response') if numerical_status == 200 else str(numerical_data.get('error'))
        contextual_text = contextual_data.get('response') if contextual_status == 200 else str(contextual_data.get('error'))

        summarized_response = summarize_responses(user_question, numerical_text, contextual_text)

        log_memory("After query_chatbot")
        return jsonify({"response": summarized_response}), 200

    except Exception as e:
        print(f"Error in query_chatbot: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500    

@app.route('/api/companies', methods=['GET'])
def fetch_companies():
    """API Endpoint to get company names"""
    return jsonify(get_company_names_from_db())

@app.route('/api/sec_reports/<company>', methods=['GET'])
def get_sec_reports(company):
    company = company.upper()

    connection = get_db_connection()

    cursor = connection.cursor()

    query = """
        SELECT quarter, filing_url
        FROM sec_filings
        WHERE UPPER(company_name) = :company
    """
    cursor.execute(query, {"company": company})
    result = cursor.fetchall()
    cursor.close()
    connection.close()

    if not result:
        return jsonify({"error": "No SEC filings found"}), 404

    reports = {row[0]: row[1] for row in result}
    return jsonify({"company": company, "reports": reports})

#----------------------------------------Key Metrics Endpoint----------------------------------------
@app.route('/api/key_metrics', methods=['GET'])
def get_key_metrics():
    """Endpoint to check key usage statistics"""
    try:
        stats = key_manager.get_usage_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#----------------------------------------Utility Functions----------------------------------------

#Summarization Function
def summarize_responses(user_question, numerical_response, contextual_response):
    """Summarize and format responses with detailed logging"""
    print("\n=== STARTING RESPONSE SUMMARIZATION ===")
    print(f"User Question: {user_question}")
    print(f"Numerical Response: {numerical_response}")
    print(f"Contextual Response: {contextual_response[:200]}...")  # Show preview
    
    # Ensure numerical_text is always a string
    numerical_str = str(numerical_response) if numerical_response else "No numerical data available"
    print(f"\n[1/3] Formatted Numerical Response: {numerical_str}")
    
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
        - Never put % unless the question mentions percentage
    - If the user asks for a **count** (like number of employees, units, or quarters), return the raw number with commas if large (`5,000`).
    - Do not repeat the question. No explanations.

    ###Inputs:
    User Question: {user_question}
    Numerical Response (SQL): {numerical_response}
    Contextual Response (RAG): {contextual_response}

    If you used the numerical response, always end with:
    "All monetary values are in millions."
"""
    print(f"\n[2/3] Generated Prompt (Preview):\n{prompt[:500]}...")  # Show first 500 chars

    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1}/{max_retries}: Querying LLM...")
            start_time = time.time()
            
            # Use the wrapper instead of direct Groq client
            response, error = GroqWrapper.make_summarize_request(
                model=model_name,
                messages=[{"role": "system", "content": prompt}],
                max_tokens=512,
                temperature=0.3
            )
            
            if error:
                raise Exception(error)
                
            latency = time.time() - start_time
            print(f"  LLM Response received in {latency:.2f}s")
            print(f"  Model: {model_name}")
            print(f"  Tokens Used: {response.usage.total_tokens if hasattr(response, 'usage') else 'N/A'}")
            print(f"  Used API Key: {response._metadata['api_key'] if hasattr(response, '_metadata') else 'Unknown'}")

            formatted_response = response.choices[0].message.content.strip()
            print(f"\n[3/3] Raw LLM Response:\n{formatted_response}")

            if not formatted_response or formatted_response.lower().startswith("error"):
                raise ValueError("Invalid response received from LLM.")

            print("\n=== SUMMARIZATION SUCCESSFUL ===")
            return formatted_response
            
        except Exception as e:
            error_message = str(e).lower()
            print(f"\n⚠️ Attempt {attempt + 1} failed with error: {error_message}")

            # Handle specific error cases with logging
            if "503" in error_message or "service unavailable" in error_message:
                print("  Detected service unavailable error")
                if attempt == max_retries - 1:
                    print("  Max retries reached for service unavailable")
                    return "We are currently experiencing high demand. Please try again later."
                time.sleep((attempt + 1) * 2)
                continue

            if "rate limit" in error_message or "too many requests" in error_message:
                print("  Detected rate limiting")
                if attempt == max_retries - 1:
                    print("  Max retries reached for rate limiting")
                    return "We are currently handling a high number of requests. Please try again in a few minutes."
                time.sleep((attempt + 1) * 2)
                continue

            if "unauthorized" in error_message or "invalid api key" in error_message:
                print("  Detected authorization error")
                return "We are currently unable to process this request. Please try again later."

            if attempt == max_retries - 1:
                print("  Max retries reached for generic error")
                return "We are experiencing technical difficulties. Please try again later."

            print(f"  Waiting {((attempt + 1) * 2)} seconds before retry...")
            time.sleep((attempt + 1) * 2)

    print("\n=== SUMMARIZATION FAILED AFTER ALL RETRIES ===")
    return "We are experiencing technical difficulties. Please try again later."


def get_ddl_prefix_from_db(company_name):
    """Fetch DDL prefix from the Oracle database mapping table."""
    connection = get_db_connection()

    cursor = connection.cursor()

    query = "SELECT DDL_PREFIX FROM COMPANY_MAPPING WHERE LOWER(COMPANY_NAME) = LOWER(:company_name)"
    cursor.execute(query, {"company_name": company_name})
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    return result[0] if result else None

def get_company_names_from_db():
    """Fetch distinct company names from the COMPANY_MAPPING table."""
    connection = get_db_connection()

    cursor = connection.cursor()
    query = "SELECT DISTINCT UPPER(COMPANY_NAME) FROM COMPANY_MAPPING"
    cursor.execute(query)
    
    companies = [row[0] for row in cursor.fetchall()]
    cursor.close()
    connection.close()
    
    return companies

# Retrieve database configuration
db_config = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "dsn": os.getenv("DB_DSN"),
    "wallet_location": os.getenv("DB_WALLET_LOCATION"),
}

def handle_numerical_query(user_question, selected_company, session_id=None):
    try:
        if not selected_company:
            return {"error": "No company selected for numerical query"}, 400
        
        ddl_directory = "Oracle_DDLs"
        model_name = "llama-3.3-70b-versatile"
        ddl_prefix = get_ddl_prefix_from_db(selected_company)

        # Get chat history if session_id is provided
        chat_history = []
        if session_id:
            with db_lock:
                chat_messages = Chat.query.filter_by(session_id=session_id).order_by(Chat.id).all()
                chat_history = [{'sender': msg.sender, 'message': msg.message} for msg in chat_messages]

        if ddl_prefix:
            ddl_file_path = os.path.join(ddl_directory, f"{ddl_prefix}_ddl.sql")
        else:
            return {"error": "Company not recognized"}, 404

        if not os.path.exists(ddl_file_path):
            return {"error": "DDL not found for the specified company"}, 404

        with open(ddl_file_path, "r", encoding="utf-8") as ddl_file:
            ddl_content = ddl_file.read().strip()

        llm_output = query_llm(user_question, ddl_content, model_name, key_manager.get_sql_key(), chat_history=chat_history)

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
                formatted_results = results
                
                print(formatted_results)
                return {"response": formatted_results}, 200
        else:
            return {"error": "Failed to extract SQL query from LLM response."}, 500
    except Exception as e:
        return {"error": str(e)}, 500
    
    
# Handle Contextual (RAG-based) Queries
def handle_contextual_query(user_question, selected_company, session_id=None):
    """Handle contextual queries using MongoDB Atlas Vector Search with conversation history."""
    try:
    
        # Get chat history if session_id is provided
        # Get chat history within the same context
        chat_history = []
        if session_id:
            with db_lock:
                chat_messages = Chat.query.filter_by(session_id=session_id).order_by(Chat.id).all()
                chat_history = [{'sender': msg.sender, 'message': msg.message} for msg in chat_messages]
        
        final_query = f"[Company: {selected_company}] {user_question}"
        response, relevant_docs = query_llm_groq(final_query, selected_company, chat_history)
        
        if isinstance(response, str) and response.startswith("❌"):
            return {"error": response}, 500

        sources = [{"source": doc["source"], "snippet": doc["text"][:200]} for doc in relevant_docs]
        return {
            "response": response,
            "sources": sources
        }, 200
    except Exception as e:
        return {"error": str(e)}, 500
    

#------------------------------------------PDF Processing---------------------------------------- 
# Dictionary to track PDF processing status
pdf_status = {}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def robust_delete(path):
    """
    Cross-platform folder deletion that handles:
    - Permission issues
    - Locked files
    - Read-only files
    - Retries with delays
    """
    def on_error(func, path, exc_info):
        # Try changing permissions and retrying
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if not os.path.exists(path):
        return

    max_retries = 3
    for attempt in range(max_retries):
        try:
            shutil.rmtree(path, onerror=on_error)
            print(f"✅ Successfully deleted {path}")
            return
        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1} failed for {path}: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))  # Exponential backoff
            else:
                raise Exception(f"Failed to delete {path} after {max_retries} attempts")

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    """User-isolated PDF upload and processing"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    user_id = str(request.form.get("user_id"))  # 🧠 Must be passed from frontend!

    if not user_id:
        return jsonify({"error": "Missing user_id in request"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Invalid file format"}), 400

    # Save under a user-specific folder
    user_upload_folder = os.path.join(UPLOAD_FOLDER, user_id)
    os.makedirs(user_upload_folder, exist_ok=True)

    file_path = os.path.join(user_upload_folder, file.filename)

    try:
        # Save PDF to user folder
        file.save(file_path)
        print(f"✅ Saved PDF for user '{user_id}' at {file_path}")
    except Exception as e:
        print(f"❌ Error saving PDF: {e}")
        return jsonify({"error": f"Failed to save file: {e}"}), 500

    # Track status by user+filename combo
    status_key = f"{user_id}:{file.filename}"
    pdf_status[status_key] = "processing"

    # Background processing thread
    def process():
        try:
            print(f"⚙️ Processing PDF for user: {user_id}")
            success = rag_system.process_pdf(file_path, user_id)
            pdf_status[status_key] = "done" if success else "failed"
        except Exception as e:
            pdf_status[status_key] = "failed"
            print(f"❌ PDF processing failed: {e}")

    threading.Thread(target=process).start()

    return jsonify({
        "message": "File uploaded! Processing in background...",
        "filename": file.filename,
        "user_id": user_id,
        "status_check": f"/pdf_status/{user_id}/{file.filename}"
    })


@app.route("/query_pdf_chatbot", methods=["POST"])
def query_pdf_chatbot():
    try:
        data = request.get_json()
        print("Received data:", data)

        question = data.get("question", "")
        user_id = data.get("user_id")
        filename = data.get("filename")

        if not question or not user_id or not filename:
            return jsonify({"response": "Missing required fields: question, user_id, or filename"}), 400

        print(f"📥 Querying for user: {user_id}, file: {filename}, question: {question}")

        # Query MongoDB vector store
        response, sources = rag_system.query_financial_data(
            query=question,
            user_id=user_id,
            filename=filename
        )

        print("✅ Response generated from Groq LLM")
        return jsonify({
            "response": response,
            "sources": sources
        })

    except Exception as e:
        print("❌ Error processing query:", str(e))
        return jsonify({"response": "Internal server error"}), 500


# API to Check PDF Processing Status
@app.route("/pdf_status/<user_id>/<filename>", methods=["GET"])
def check_pdf_status(user_id, filename):
    """Check PDF processing status for a specific user and file."""
    status_key = f"{user_id}:{filename}"
    status = pdf_status.get(status_key, "not_found")
    return jsonify({"status": status})

#----------------------------------------Show Company Metrics----------------------------------
def get_metrics_for_company(company_name):
    """Fetch available metrics from all financial tables for a selected company."""
    ddl_prefix = get_ddl_prefix_from_db(company_name)
    
    if not ddl_prefix:
        print(f"DEBUG: No DDL_PREFIX found for {company_name}")
        return {"error": f"No DDL_PREFIX found for {company_name}"}, 404

    # Convert DDL_PREFIX to uppercase to match the table names in Oracle
    ddl_prefix = ddl_prefix.upper()

    tables = [
        f"{ddl_prefix}_BALANCE_SHEET_QUARTERLY",
        f"{ddl_prefix}_CASH_FLOW_QUARTERLY",
        f"{ddl_prefix}_INCOME_QUARTERLY",
        f"{ddl_prefix}_RATIO_QUARTERLY"
    ]
    
    metrics_set = set()

    connection = get_db_connection()

    cursor = connection.cursor()

    try:
        for table in tables:
            query = f'SELECT DISTINCT METRICS FROM "{table}"'
            print(f"DEBUG: Executing query → {query}")  
            cursor.execute(query)
            
            fetched_rows = cursor.fetchall()
            print(f"DEBUG: Results from {table} → {fetched_rows}")  # Print actual results

            metrics_set.update(row[0] for row in fetched_rows if row[0] is not None)

    except Exception as e:
        print(f"ERROR: Failed to fetch metrics for {company_name} → {str(e)}")
        return {"error": str(e)}, 500
    finally:
        cursor.close()
        connection.close()

    return {"metrics": list(metrics_set)}, 200

@app.route('/api/company_metrics/<company_name>', methods=['GET'])
def fetch_company_metrics(company_name):
    """API endpoint to get all available metrics for a company."""
    company_name = company_name.upper()  # Normalize input
    response = get_metrics_for_company(company_name)

    print(f"DEBUG: API Response Sent → {response}")  # Log API output

    return jsonify(response)  # Only return JSON object (removes tuple)

@app.route('/')
def index():
 return '✅ Backend is running fine!', 200


#----------------------------------------Main Execution----------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5050))  # Default to 10000 if PORT is not set
    app.run(debug=False, host='0.0.0.0', port=port)