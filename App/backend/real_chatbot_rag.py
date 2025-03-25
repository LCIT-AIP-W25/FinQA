import os
import re
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_groq import ChatGroq
from groq import Groq
from bs4 import BeautifulSoup
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Load environment variables
load_dotenv()

# Configuration
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Global variables for initialized components
_initialized = False
_collection = None
_embeddings = None
_vector_store = None

# ------------------- Initialization (Run Once) ------------------- #
def initialize_components():
    """Initialize all components once at application startup."""
    global _initialized, _collection, _embeddings, _vector_store
    
    if _initialized:
        return True
    
    try:
        # 1. MongoDB Connection
        _collection = connect_to_mongo()
        if _collection is None:
            return False
        
        # 2. Embeddings Model
        _embeddings = init_embeddings()
        if _embeddings is None:
            return False
            
        # 3. Vector Store
        _vector_store = MongoDBAtlasVectorSearch(
            collection=_collection,
            embedding=_embeddings,
            index_name="st_vector_index",
            embedding_key="embedding",
            text_key="content"
        )
        
        # Test the vector store
        _vector_store.similarity_search("test", k=1)
        
        _initialized = True
        print("✅ All components initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False

# ------------------- MongoDB Connection ------------------- #
def connect_to_mongo():
    """Establish connection to MongoDB Atlas (called once during init)."""
    try:
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in .env file")
        
        client = MongoClient(MONGO_URI)
        db = client["Financial_Rag_DB"]
        collection = db["test_files"]
        
        # Verify connection
        count = collection.estimated_document_count()
        print(f"✅ Connected to MongoDB Atlas - {count} documents found")
        return collection
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

# ------------------- Embeddings ------------------- #
def init_embeddings():
    """Initialize the embeddings model (called once during init)."""
    try:
        embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-cos-v1")
        print("✅ Embeddings model initialized")
        return embeddings
    except Exception as e:
        print(f"❌ Embeddings initialization failed: {e}")
        return None

# ------------------- Document Processing ------------------- #
def financial_preprocessor(text):
    """Remove HTML tags and URLs (called per query)."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()

def retrieve_documents(query, selected_company=None, k=4):
    """
    Retrieve relevant documents (called per query).
    Uses the pre-initialized vector store.
    """
    if not _initialized:
        raise RuntimeError("Components not initialized")
    
    filter_query = None
    if selected_company and selected_company != "All":
        filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}_Q[1-4] \\d{{4}}\\.txt$", "$options": "i"}}
    
    try:
        retrieved_docs = _vector_store.similarity_search(query, k=k, filter=filter_query)
        
        # Additional company filter as a safeguard
        if selected_company and selected_company != "All":
            retrieved_docs = [
                doc for doc in retrieved_docs
                if doc.metadata.get("company_id", "").lower().startswith(selected_company.lower())
            ]
        
        return [
            {"text": doc.page_content, "source": doc.metadata.get("company_id", "Unknown Source")}
            for doc in retrieved_docs
        ]
    except Exception as e:
        print(f"❌ Retrieval Error: {str(e)}")
        return []

def query_llm_groq(final_query, selected_company=None, chat_history=None):
    """Queries Groq API with context and limited chat history."""
    if not _initialized:
        raise RuntimeError("Components not initialized")
    
    try:
        # Retrieve relevant documents
        relevant_docs = retrieve_documents(final_query, selected_company)
        
        if not relevant_docs:
            return "No relevant documents found for the query.", []

        retrieved_text = "\n\n".join([doc["text"][:400] + "..." for doc in relevant_docs])
        
        # Format only the last 5 messages if provided
        history_messages = []
        if chat_history:
            last_5_messages = chat_history[-5:]  # Get only the last 5 messages
            for msg in last_5_messages:
                role = "assistant" if msg['sender'] == 'bot' else "user"
                history_messages.append({"role": role, "content": msg['message']})
        
        # Prepare the messages for Groq API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a financial AI assistant that provides concise answers based on:"
                    "\n1. Retrieved documents (below)"
                    "\n2. The last few messages of our conversation"
                    "\n\nBe factual and professional in your responses."
                )
            }
        ]
        
        # Add limited chat history if available
        messages.extend(history_messages)
        
        # Add the current query and context
        messages.append({
            "role": "user",
            "content": (
                "Context from documents:\n"
                f"{retrieved_text}\n\n"
                f"My question: {final_query}"
            )
        })
        
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=messages,
            temperature=0.3,
            max_tokens=512,
            top_p=1,
            stream=False,
        )
        return response.choices[0].message.content, relevant_docs
    except Exception as e:
        return f"❌ Groq API Error: {str(e)}", []
    
# At the very end of real_chatbot_rag.py
if __name__ != "__main__":
    # Auto-initialize when imported as a module
    initialize_components()