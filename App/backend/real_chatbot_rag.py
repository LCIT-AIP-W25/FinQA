import os
import re
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from groq import Groq
from bs4 import BeautifulSoup
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import random

# Load environment variables
load_dotenv()
def get_random_api_key(env_var):
    keys = os.getenv(env_var)
    if not keys:
        return None
    
    # Clean and split the keys
    key_list = [key.strip().strip('"').strip("'").strip() for key in keys.split(",")]
    key_list = [key for key in key_list if key]  # Remove empty strings
    
    if not key_list:
        return None
    
    return random.choice(key_list)

# Configuration
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
MONGO_URI = os.getenv("MONGO_URI")


# Global variables for initialized components
_initialized = False
_collection = None
_embeddings = None
_vector_store = None


# Hardcoded mapping between selected company names and their MongoDB company_id prefixes
COMPANY_MAPPING = {
    "AMAZON": "Amazon",
    "AMD": "AMD",
    "ATT": "AT&T",  # Maps "ATT" to "AT&T" in database
    "GOOGLE": "Google",
    "JPMORGAN": "JP Morgan",  # Maps "JPMORGAN" to "JP Morgan"
    "MASTERCARD": "Mastercard",
    "MCDONALDS": "McDonald",  # Note the different spelling
    "META": "Meta",
    "PEPSICO": "Pepsico",
    "S&P GLOBAL": "S&P Global",  # Handles the special characters
    "TESLA": "Tesla",
    # Add any other companies you need to support
}

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
            index_name="vector_index_g",
            embedding_key="embedding",
            text_key="content"
        )
        print("✅ Vector store created with config:")
        print(f"   - Index name: vector_index_g")
        print(f"   - Embedding key: embedding")
        print(f"   - Text key: content")
        
        _initialized = True
        print("\n=== ✅ ALL COMPONENTS INITIALIZED SUCCESSFULLY ===")
        return True
        
    except Exception as e:
        print(f"\n=== ❌ INITIALIZATION FAILED ===")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def connect_to_mongo():
    """Establish connection to MongoDB Atlas (called once during init)."""
    try:
        print("   Checking MONGO_URI...")
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in .env file")
        
        print("   Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client["Financial_Rag_DB"]
        collection = db["chunks_data"]
        
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

def init_embeddings():
    """Initialize the embeddings model (called once during init)."""
    try:
        print("   Checking GOOGLE_API_KEY...")
        GOOGLE_API_KEY = get_random_api_key("GOOGLE_API_KEY")  # Using primary key for query operations
        print("API Google:",GOOGLE_API_KEY)
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
    

def create_company_filter(selected_company):
    """Create a MongoDB filter using the hardcoded mapping"""
    if not selected_company or selected_company == "All":
        return None
    
    # Get the standardized prefix from our mapping
    mapped_prefix = COMPANY_MAPPING.get(selected_company.upper())
    
    if not mapped_prefix:
        print(f"⚠️ No mapping found for company: {selected_company}")
        return None
    
    # Create regex pattern that matches the standardized prefix followed by underscore
    regex_pattern = f"^{re.escape(mapped_prefix)}_"
    
    return {"company_id": {"$regex": regex_pattern, "$options": "i"}}

# Updated retrieve_documents function using the direct mapping
def retrieve_documents(query, selected_company=None, k=4):
    """
    Retrieve documents using the direct company mapping
    """
    print(f"\n=== DOCUMENT RETRIEVAL ===")
    print(f"Query: '{query}'")
    print(f"Company filter: '{selected_company}'")
    
    if not _initialized:
        raise RuntimeError("Components not initialized")
    
    try:
        filter_query = create_company_filter(selected_company)
        if filter_query:
            print(f"🔍 Using mapped filter: {filter_query}")
        
        # Get extra docs in case client-side filtering is needed
        retrieved_docs = _vector_store.similarity_search(
            query, 
            k=k*2,  
            filter=filter_query
        )
        
        # Additional client-side verification using the mapping
        if selected_company and selected_company != "All":
            mapped_prefix = COMPANY_MAPPING.get(selected_company.upper())
            if mapped_prefix:
                retrieved_docs = [
                    doc for doc in retrieved_docs
                    if str(doc.metadata.get("company_id", "")).startswith(mapped_prefix + "_")
                ]
        
        # Sort and limit results
        retrieved_docs.sort(key=lambda d: d.metadata.get("sequence", 0))
        retrieved_docs = retrieved_docs[:k]
        
        # Prepare results
        results = [
            {
                "text": doc.page_content,
                "source": f"{doc.metadata.get('company_id', 'Unknown')} | Chunk: {doc.metadata.get('chunk_id', '?')}"
            }
            for doc in retrieved_docs
        ]
        
        print(f"\n✅ Retrieved {len(results)} documents")
        return results
        
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
        GROQ_API_KEY_RAG = get_random_api_key("GROQ_API_KEY_RAG")
        print("\nSending to Groq API...")
        client = Groq(api_key=GROQ_API_KEY_RAG)
        print("API Key RAG:",GROQ_API_KEY_RAG)
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