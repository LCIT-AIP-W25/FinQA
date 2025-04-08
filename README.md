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

