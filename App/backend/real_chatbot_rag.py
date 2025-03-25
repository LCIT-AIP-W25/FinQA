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

# ------------------- MongoDB Connection ------------------- #
def connect_to_mongo():
    """Establish connection to MongoDB Atlas."""
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGO_URI not found in .env file")
        
        client = MongoClient(mongo_uri)
        db = client["Financial_Rag_DB"]
        collection = db["test_files"]
        # Verify connection by performing a simple operation
        collection.count_documents({}, limit=1)  # This will raise an exception if connection fails
        print("✅ Connected to MongoDB Atlas")
        return collection
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

def validate_mongo_connection(collection):
    """Validate the MongoDB connection by checking document count."""
    try:
        count = collection.estimated_document_count()
        print(f"✅ MongoDB Collection validated: {count} documents found")
        return True
    except Exception as e:
        print(f"❌ MongoDB validation failed: {e}")
        return False

# ------------------- Embeddings ------------------- #
def init_embeddings():
    """Initialize the Sentence Transformer embeddings model."""
    embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-cos-v1")
    return embeddings

# ------------------- Vector Store ------------------- #
def load_vector_store():
    """Load the MongoDB Atlas vector store."""
    try:
        collection = connect_to_mongo()
        if collection is None:  # Explicit None check
            return None
        
        # Verify the collection exists and is accessible
        if not validate_mongo_connection(collection):
            return None
        
        embeddings = init_embeddings()
        if embeddings is None:
            return None
            
        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name="st_vector_index",
            embedding_key="embedding",
            text_key="content"
        )
        
        # Test the vector store with a simple query
        try:
            vector_store.similarity_search("test", k=1)
            print("✅ Vector store initialized and validated")
            return vector_store
        except Exception as e:
            print(f"❌ Vector store test query failed: {e}")
            return None
            
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        return None

# ------------------- Document Processing ------------------- #
def financial_preprocessor(text):
    """Remove HTML tags and URLs."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()

def retrieve_documents(vector_store, query, selected_company=None, k=4):
    """
    Retrieve relevant documents from MongoDB Atlas Vector Search.
    """
    filter_query = None
    if selected_company and selected_company != "All":
        # Construct regex to match company_id format
        filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}_Q[1-4] \\d{{4}}\\.txt$", "$options": "i"}}
    
    try:
        retrieved_docs = vector_store.similarity_search(query, k=k, filter=filter_query)
        
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

# ------------------- LLM Query ------------------- #
def query_llm_groq(final_query, retriever, selected_company=None):
    """Queries Groq API with context from MongoDB vector store."""
    try:
        relevant_docs = retrieve_documents(retriever, final_query, selected_company)
        
        if not relevant_docs:
            return "No relevant documents found for the query.", []

        retrieved_text = "\n\n".join([doc["text"][:400] + "..." for doc in relevant_docs])

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="mistral-saba-24b",
            messages=[{
                "role": "user",
                "content": (
                    "You are a financial AI assistant that provides concise answers based on retrieved documents.\n"
                    "Based on the following retrieved information, answer the question:\n\n"
                    f"{retrieved_text}\n\nQuestion: {final_query}"
                )
            }],
            temperature=0.3,
            max_tokens=512,
            top_p=1,
            stream=False,
        )
        return response.choices[0].message.content, relevant_docs
    except Exception as e:
        return f"❌ Groq API Error: {str(e)}", []

