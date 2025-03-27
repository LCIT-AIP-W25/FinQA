import os
import re
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from groq import Groq
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Configuration
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Using primary key for query operations

# Global variables for initialized components
_initialized = False
_collection = None
_embeddings = None
_vector_store = None

# ------------------- Initialization (Run Once) ------------------- #
def initialize_components():
    """Initialize all components once at application startup."""
    global _initialized, _collection, _embeddings, _vector_store
    
    print("\n=== INITIALIZATION STARTED ===")
    
    if _initialized:
        print("⚠️ Components already initialized")
        return True
    
    try:
        print("\n[1/3] Attempting MongoDB connection...")
        _collection = connect_to_mongo()
        if _collection is None:
            print("❌ MongoDB connection failed")
            return False
        print(f"✅ MongoDB connected. Collection: {_collection.name}")
        
        print("\n[2/3] Initializing embeddings model...")
        _embeddings = init_embeddings()
        if _embeddings is None:
            print("❌ Embeddings initialization failed")
            return False
        print(f"✅ Embeddings model ready: {type(_embeddings).__name__}")
            
        print("\n[3/3] Creating vector store...")
        _vector_store = MongoDBAtlasVectorSearch(
            collection=_collection,
            embedding=_embeddings,
            index_name="st_vector_index",
            embedding_key="embedding",
            text_key="content"
        )
        print("✅ Vector store created with config:")
        print(f"   - Index name: st_vector_index")
        print(f"   - Embedding key: embedding")
        print(f"   - Text key: content")
        
        print("\n🧪 Testing vector store with sample query...")
        test_results = _vector_store.similarity_search("test", k=1)
        print(f"Test query returned {len(test_results)} results")
        if test_results:
            print(f"Sample result metadata: {test_results[0].metadata}")
        
        _initialized = True
        print("\n=== ✅ ALL COMPONENTS INITIALIZED SUCCESSFULLY ===")
        return True
        
    except Exception as e:
        print(f"\n=== ❌ INITIALIZATION FAILED ===")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# ------------------- MongoDB Connection ------------------- #
def connect_to_mongo():
    """Establish connection to MongoDB Atlas (called once during init)."""
    try:
        print("   Checking MONGO_URI...")
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in .env file")
        
        print("   Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client["Financial_Rag_DB"]
        collection = db["test_files"]
        
        print("   Verifying connection...")
        count = collection.estimated_document_count()
        print(f"   Found {count} documents in collection")
        
        # Check if any documents have embeddings
        embedded_count = collection.count_documents({"embedding": {"$exists": True}})
        print(f"   Documents with embeddings: {embedded_count}/{count}")
        
        if embedded_count == 0:
            print("   ⚠️ WARNING: No documents have embeddings - retrieval will fail!")
        
        return collection
        
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return None

# ------------------- Embeddings ------------------- #
def init_embeddings():
    """Initialize the embeddings model (called once during init)."""
    try:
        print("   Checking GOOGLE_API_KEY...")
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in .env file")
        
        print("   Creating embeddings model...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
        
        print("   Testing embeddings with sample text...")
        sample_text = "This is a test document."
        embedding = embeddings.embed_query(sample_text)
        print(f"   Embedding generated. Dimension: {len(embedding)}")
        print(f"   First 5 values: {embedding[:5]}")
        
        return embeddings
    except Exception as e:
        print(f"   ❌ Initialization failed: {e}")
        return None

# ------------------- Document Processing ------------------- #
def financial_preprocessor(text):
    """Remove HTML tags and URLs (called per query)."""
    print("\n=== DOCUMENT PREPROCESSING ===")
    print(f"Original text length: {len(text)}")
    text = BeautifulSoup(text, "html.parser").get_text()
    print(f"After HTML parsing: {len(text)}")
    text = URL_PATTERN.sub('', text)
    print(f"After URL removal: {len(text)}")
    return text.strip()

def retrieve_documents(query, selected_company=None, k=4):
    """
    Retrieve relevant documents (called per query).
    Uses the pre-initialized vector store.
    """
    print("\n=== DOCUMENT RETRIEVAL STARTED ===")
    print(f"Query: '{query}'")
    print(f"Company filter: '{selected_company}'")
    print(f"Requested documents: {k}")
    
    if not _initialized:
        raise RuntimeError("Components not initialized")
    
    filter_query = None
    if selected_company and selected_company != "All":
        # Simplified regex pattern - just checks if company_id starts with company name
        filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}", "$options": "i"}}
        print(f"Generated filter query: {filter_query}")
    
    try:
        print("\nExecuting similarity search...")
        retrieved_docs = _vector_store.similarity_search(query, k=k, filter=filter_query)
        print(f"Found {len(retrieved_docs)} documents")
        
        if not retrieved_docs:
            print("⚠️ No documents found")
        else:
            print("Retrieved documents metadata:")
            for i, doc in enumerate(retrieved_docs, 1):
                print(f"{i}. {doc.metadata.get('company_id', 'Unknown')} - {len(doc.page_content)} chars")
        
        return [
            {"text": doc.page_content, "source": doc.metadata.get("company_id", "Unknown Source")}
            for doc in retrieved_docs
        ]
    except Exception as e:
        print(f"❌ Retrieval Error: {str(e)}")
        return []

def query_llm_groq(final_query, selected_company=None, chat_history=None):
    """Queries Groq API with context and limited chat history."""
    print("\n=== LLM QUERY STARTED ===")
    print(f"Final query: '{final_query}'")
    print(f"Selected company: '{selected_company}'")
    print(f"Chat history length: {len(chat_history) if chat_history else 0}")
    
    if not _initialized:
        raise RuntimeError("Components not initialized")
    
    try:
        print("\n[1/3] Retrieving relevant documents...")
        relevant_docs = retrieve_documents(final_query, selected_company)
        
        if not relevant_docs:
            print("⚠️ No relevant documents found")
            return "No relevant documents found for the query.", []
        
        print("\n[2/3] Preparing context...")
        retrieved_text = "\n\n".join([doc["text"][:400] + "..." for doc in relevant_docs])
        print(f"Context length: {len(retrieved_text)} characters")
        
        history_messages = []
        if chat_history:
            print("Processing chat history...")
            last_5_messages = chat_history[-5:]
            print(f"Using last {len(last_5_messages)} messages from history")
            for msg in last_5_messages:
                role = "assistant" if msg['sender'] == 'bot' else "user"
                history_messages.append({"role": role, "content": msg['message']})
        
        print("\n[3/3] Building messages for Groq API...")
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
        
        if history_messages:
            messages.extend(history_messages)
            print(f"Added {len(history_messages)} history messages")
        
        messages.append({
            "role": "user",
            "content": (
                "Context from documents:\n"
                f"{retrieved_text}\n\n"
                f"My question: {final_query}"
            )
        })
        
        print("\nSending to Groq API...")
        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=messages,
            temperature=0.3,
            max_tokens=512,
            top_p=1,
            stream=False,
        )
        
        print("✅ LLM response received")
        return response.choices[0].message.content, relevant_docs
    except Exception as e:
        print(f"❌ Groq API Error: {str(e)}")
        return f"❌ Groq API Error: {str(e)}", []
    
# At the very end of real_chatbot_rag.py
if __name__ != "__main__":
    # Auto-initialize when imported as a module
    print("=== SCRIPT IMPORTED - INITIALIZING ===")
    initialize_components()