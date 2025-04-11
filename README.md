# FinQA - Financial Question Answering System  

A full-stack application that leverages **Groq AI**, **Google Embeddings**, and databases (Oracle, PostgreSQL, MongoDB) to provide financial insights via natural language queries.  

## 🛠 Prerequisites  
Before you begin, ensure you have the following installed:  
- **Python 3.9+** (for backend)  
- **Node.js & npm** (for frontend)  
- **PostgreSQL** (or a remote DB URI)  
- **MongoDB** (or a remote URI)  
- **Oracle DB Wallet** (if using Oracle)  
- **Git**  

## 🚀 Setup & Installation  

### 1. Clone the Repository  
```sh
git clone https://github.com/LCIT-AIP-W25/FinQA.git
cd FinQA
```

### 2. Set Up Backend Environment  
#### Create & Activate a Python Virtual Environment  
```sh
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

#### Install Python Dependencies  
```sh
pip install -r requirements.txt
```

## 🗃️ MongoDB Setup

Our project uses **MongoDB Atlas** for storing and retrieving vector-based embeddings of financial reports. It supports fast and semantic search through vector indexing.

### 🔧 Collections Overview

The MongoDB database is named `Financial_Rag_DB` and includes two collections:

- `chunks_data`: For structured financial reports of companies.
- `finqa_pdf`: For user-uploaded PDFs.

---

### 1. 📁 `chunks_data` Collection

This collection stores vector embeddings of company-specific financial documents segmented into chunks.

**Sample Document Schema:**
```json
{
  "_id": ObjectId("..."),
  "company_id": "AMD_Q4 2023.txt",
  "chunk_id": "AMD_Q4 2023.txt_1",
  "content": "BUSINESS Cautionary Statement Regarding Forward-Looking Statements...",
  "sequence": 1,
  "text": "",
  "embedding": [768-dimensional vector]
}
```

**Vector Index Configuration (vector_index_g):**
```json
{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "company_id"
    }
  ]
}
```

## 📁 finqa_pdf Collection
This collection handles personalized data from user-uploaded PDFs, chunked, embedded, and stored securely by user_id and filename.

**Sample Document Schema:**

```json
{
  "_id": ObjectId("..."),
  "user_id": "10",
  "filename": "sddsfsdf.pdf",
  "content": "• Conducted in-depth data analysis using Python and SQL...",
  "metadata": {
    "page": 1,
    "section": "other",
    "type": "text",
    "chunk_id": 2
  },
  "embedding": [768-dimensional vector]
}
```

**Vector Index Configuration (vector_index_pdf):**

```json

{
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 768,
      "similarity": "cosine"
    },
    {
      "type": "filter",
      "path": "user_id"
    },
    {
      "type": "filter",
      "path": "filename"
    }
  ]
}
```
---

## 🧮 Oracle Database Setup

We use **Oracle Autonomous Database** to store structured financial data for each company in tabular format. Each company has its own table containing financial metrics over multiple quarters.

### 🏛️ Table Schema

### 📄 Table Schema

All company tables follow the same format:

```sql
CREATE TABLE "ADMIN"."Company_name_table_name"  
(    
  "METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP",  
  "Q3_2024" FLOAT(126),  
  "Q2_2024" FLOAT(126),  
  "Q1_2024" FLOAT(126),  
  "Q4_2023" FLOAT(126),  
  "Q3_2023" FLOAT(126),  
  "Q2_2023" FLOAT(126),  
  "Q1_2023" FLOAT(126),  
  "Q4_2022" FLOAT(126),  
  "Q3_2022" FLOAT(126)
);
```
**Description**
METRICS: Describes the financial metric (e.g., Net Income, Revenue, EBITDA, etc.)

Each quarterly column (Q3_2024, Q2_2024, etc.) stores the value of the corresponding metric in that quarter.

**🛠️ Access Configuration**
To connect the Oracle DB in your environment:

Place your Oracle Wallet in a local folder, e.g., wallet/.

Set the following environment variables in your .env file:
```env
DB_USER=your_admin_user
DB_PASSWORD=your_db_password
DB_DSN=your_db_dsn_from_wallet
DB_WALLET_LOCATION=./wallet
```

Ensure that your backend code is configured to load the wallet using Oracle's Python driver (oracledb) 

---

## 🐘 PostgreSQL Setup

We use **PostgreSQL** to manage user authentication, session tracking, and chat history. This relational database handles all user-side interactions such as login, conversation context, and account recovery.

### 🧾 Tables and SQLAlchemy Models

The schema is automatically generated via SQLAlchemy ORM. Below is a breakdown of the key tables and their structure.

---

### 📘 `User` Table

Stores information about each registered user.

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
```

### 📘 `ChatSession` Table
Tracks individual chat sessions initiated by users.

```python
class ChatSession(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100))
    user_id = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=dt.utcnow)
```

### 📘 `Chat` Table
Stores each message sent in a session, either by the user or the bot.


```python
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(10))  # 'user' or 'bot'
    message = db.Column(db.Text)
    session_id = db.Column(db.String(50), db.ForeignKey('chat_session.id'))
    created_at = db.Column(db.DateTime, default=dt.utcnow)
```

## 🔐 PostgreSQL Configuration
To set up PostgreSQL in your local or cloud environment:

Ensure PostgreSQL is installed and running.
Create a database (e.g., finqa).
Update your .env file with your connection URI:

```env
POSTGRES_URI=postgresql+psycopg2://username:password@host:port/finqa
```
On first run, your tables will be automatically created by SQLAlchemy if they don't exist.

---

## ✉️ SendGrid Email Setup

We use **SendGrid SMTP** to send verification, reset, and notification emails to users. This integration is handled via the `Flask-Mail` extension in the `auth_app`.

### 📦 Configuration Code

The following environment variables are loaded into the Flask config inside `auth_app.py`:

```python
# Configure SendGrid SMTP for Email Sending
auth_app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.sendgrid.net')
auth_app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
auth_app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
auth_app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'apikey')  # Default SendGrid user
auth_app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')            # Your SendGrid API Key
auth_app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
```
## 🔐 Environment Variables
Add the following variables to your .env file in the backend/ directory:

```env
# SendGrid Email Setup
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your_sendgrid_api_key
MAIL_DEFAULT_SENDER=your_verified_sender_email@example.com

```
✅ Note: Ensure that your sender email (MAIL_DEFAULT_SENDER) is verified in your SendGrid dashboard before sending emails.

#### Configure Environment Variables  
Create a `.env` file in the `backend` folder with the following variables:  
```env
# API Keys for Groq & Google
GROQ_API_KEY_RAG=api1,api2,api3
GROQ_API_KEY_SQL=api1,api2,api3
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY_SUMMARIZE=api1,api2,api3

# OracleDB Wallet Configuration
DB_USER=
DB_PASSWORD=
DB_DSN=
DB_WALLET_LOCATION=

# PostgreSQL URI
POSTGRES_URI=

# MongoDB URI
MONGO_URI=

# SendGrid Email Setup
MAIL_SERVER=
MAIL_PORT=
MAIL_USE_TLS=
MAIL_USE_SSL=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=
```

### 3. Set Up Frontend  
#### Install Node.js Dependencies  
```sh
cd ../App  # Move to the frontend directory
npm install
```

## 🖥 Running the Application  
You need **three terminals** running simultaneously:  

### Terminal 1: Backend (Auth Server)  
```sh
cd backend
source venv/bin/activate  # Activate env (Linux/Mac)
python auth_app.py
```

### Terminal 2: Backend (Main Server)  
```sh
cd backend
source venv/bin/activate  # Activate env (Linux/Mac)
python app.py
```

### Terminal 3: Frontend (React App)  
```sh
cd App  # Ensure you're in the frontend directory
npm start
```

The frontend should open automatically at `http://localhost:3000`.  

## 🔧 Troubleshooting  
- **Python Module Errors?** → Reinstall dependencies (`pip install -r requirements.txt`).  
- **Node.js Issues?** → Delete `node_modules` and reinstall (`npm install`).  
- **Database Connection Failing?** → Verify `.env` credentials and DB accessibility.  

## 📜 License  
This project is under the [MIT License](LICENSE).  
