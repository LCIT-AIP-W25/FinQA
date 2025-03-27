

import os
import re
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from bs4 import BeautifulSoup
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_groq import ChatGroq
from groq import Groq
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

# Configuration
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Google API key rotation list
GOOGLE_API_KEYS = [
    os.getenv("GOOGLE_API_KEY1"),
    os.getenv("GOOGLE_API_KEY2"),
    os.getenv("GOOGLE_API_KEY3"),
]

# Global variables
_initialized = False
_collection = None
_vector_store = None


def get_rotated_embedding():
    """Initialize embedding with rotated Google API key."""
    key_index = int(time.time()) % len(GOOGLE_API_KEYS)
    current_key = GOOGLE_API_KEYS[key_index]
    try:
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=current_key
        )
    except Exception as e:
        print(f"❌ Error initializing embedding with key #{key_index + 1}: {e}")
        return None


def initialize_components():
    global _initialized, _collection, _vector_store
    if _initialized:
        return True

    try:
        _collection = connect_to_mongo()
        if _collection is None:
            return False
        _initialized = True
        print("✅ All components initialized successfully")
        return True

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return False


def connect_to_mongo():
    try:
        if not MONGO_URI:
            raise ValueError("MONGO_URI not found in .env file")

        client = MongoClient(MONGO_URI)
        db = client["Financial_Rag_DB"]
        collection = db["chunks_data"]
        count = collection.estimated_document_count()
        print(f"✅ Connected to MongoDB Atlas - {count} documents found")
        return collection

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None


def financial_preprocessor(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()


def retrieve_documents(query, selected_company=None, k=5):
    if not _initialized:
        raise RuntimeError("Components not initialized")

    embeddings = get_rotated_embedding()
    if not embeddings:
        return []

    try:
        vector_store = MongoDBAtlasVectorSearch(
            collection=_collection,
            embedding=embeddings,
            index_name="vector_index_g",
            embedding_key="embedding",
            text_key="content"
        )

        filter_query = None
        if selected_company and selected_company != "All":
            filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}.*", "$options": "i"}}

        retrieved_docs = vector_store.similarity_search(query, k=15, filter=filter_query)

        if selected_company and selected_company != "All":
            retrieved_docs = [
                doc for doc in retrieved_docs
                if doc.metadata.get("company_id", "").lower().startswith(selected_company.lower())
            ]

        # Sort by sequence to maintain logical order within company chunks
        retrieved_docs.sort(key=lambda d: d.metadata.get("sequence", 0))

        return [
            {"text": doc.page_content, "source": f"{doc.metadata.get('company_id')} | Chunk: {doc.metadata.get('chunk_id')}"}
            for doc in retrieved_docs[:k]
        ]

    except Exception as e:
        print(f"❌ Retrieval Error: {str(e)}")
        return []


def estimate_tokens(text):
    # Rough estimate: 1 token ≈ 4 characters
    return len(text) // 4


def query_llm_groq(final_query, selected_company=None, chat_history=None):
    if not _initialized:
        raise RuntimeError("Components not initialized")

    try:
        relevant_docs = retrieve_documents(final_query, selected_company)
        if not relevant_docs:
            return "No relevant documents found for the query.", []

        # Initially include all retrieved text
        retrieved_text = "\n\n".join([doc["text"] + "..." for doc in relevant_docs])

        history_messages = []
        if chat_history:
            for msg in chat_history[-5:]:
                role = "assistant" if msg['sender'] == 'bot' else "user"
                history_messages.append({"role": role, "content": msg['message']})

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
        ] + history_messages + [{
            "role": "user",
            "content": f"Context from documents:\n{retrieved_text}\n\nMy question: {final_query}"
        }]

        # Calculate total token count
        total_text = "\n".join([m["content"] for m in messages])
        total_tokens = estimate_tokens(total_text)
        token_limit = 5800  # Adjusted buffer for safety

        # If over limit, dynamically trim retrieved_text
        if total_tokens > token_limit:
            excess_tokens = total_tokens - token_limit
            chars_to_remove = excess_tokens * 4
            current_chars = len(retrieved_text)
            new_chars = max(current_chars - chars_to_remove, 50)  # Reduced minimum
            retrieved_text = retrieved_text[:new_chars] + "..." if new_chars < current_chars else retrieved_text

            # Update user message and recheck
            messages[-1]["content"] = f"Context from documents:\n{retrieved_text}\n\nMy question: {final_query}"
            total_text = "\n".join([m["content"] for m in messages])
            total_tokens = estimate_tokens(total_text)

        print(f"Estimated tokens: {total_tokens}")

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="qwen-2.5-coder-32b",
            messages=messages,
            temperature=0.3,
            max_tokens=512,
            top_p=1,
            stream=False,
        )
        return response.choices[0].message.content, relevant_docs

    except Exception as e:
        return f"❌ Groq API Error: {str(e)}", []

if __name__ == "__main__":
    if initialize_components():
        query = input("Enter your financial question: ")
        company = input("Enter company name (or leave blank for all): ") or None

        answer, sources = query_llm_groq(query, selected_company=company)

        print("\n💡 Answer:")
        print(answer)

        print("\n📄 Sources:")
        for i, doc in enumerate(sources, 1):
            print(f"{i}. Source: {doc['source']}")
            print(f"    Text Preview: {doc['text'][:120]}...\n")