import os
import re
import time
from dotenv import load_dotenv
from pymongo import MongoClient
from bs4 import BeautifulSoup
from langchain_mongodb import MongoDBAtlasVectorSearch
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

# Company name mapping
COMPANY_MAPPING = {
    "AMAZON": "Amazon",
    "AMD": "AMD",
    "ATT": "AT&T",
    "GOOGLE": "Google",
    "JPMORGAN": "JP Morgan",
    "MASTERCARD": "Mastercard",
    "MCDONALDS": "McDonald",
    "META": "Meta",
    "PEPSICO": "Pepsico",
    "S&P GLOBAL": "S&P Global",
    "TESLA": "Tesla",
    "NETFLIX": "Netflix",
    "COCACOLA": "CocaCola"
}

# Globals
_initialized = False
_collection = None
_vector_store = None

def get_rotated_embedding():
    for i, current_key in enumerate(GOOGLE_API_KEYS):
        if not current_key:
            continue
        try:
            os.environ["GOOGLE_API_KEY"] = current_key
            return GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=current_key
            )
        except Exception as e:
            print(f"❌ Error initializing embedding with key #{i + 1}: {e}")
    return None

def create_company_filter(selected_company):
    if not selected_company or selected_company.lower() == "all":
        return None
    mapped_prefix = COMPANY_MAPPING.get(selected_company.upper())
    if not mapped_prefix:
        print(f"⚠️ No mapping found for: {selected_company}")
        return None
    return {"company_id": {"$regex": f"^{re.escape(mapped_prefix)}", "$options": "i"}}

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

        print(f"✅ Connected to MongoDB Atlas - {collection.estimated_document_count()} documents found")
        print(f"🔍 Documents without embeddings: {collection.count_documents({'embedding': {'$exists': False}})}")
        print("🔗 Indexes available:")
        print(collection.index_information())

        print("📦 Sample company_ids in DB:")
        for doc in collection.find({}, {"company_id": 1}).limit(10):
            print(" -", doc.get("company_id"))
        return collection

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

def financial_preprocessor(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    return URL_PATTERN.sub('', text).strip()

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
            index_name="vector_index",
            embedding_key="embedding",
            text_key="content"
        )

        print(f"🔎 Searching MongoDB → DB: Financial_Rag_DB | Collection: chunks_data")

        filter_query = create_company_filter(selected_company)
        print(f"🔍 Using filter: {filter_query}")

        if filter_query:
            matches = list(_collection.find(filter_query, {"company_id": 1}).limit(10))
            print("🧪 Matched company_ids:")
            for doc in matches:
                print(" -", doc.get("company_id"))

        if filter_query:
            retrieved_docs = vector_store.similarity_search(
                query, k=15, search_kwargs={"filter": filter_query})
        else:
            retrieved_docs = vector_store.similarity_search(query, k=15)

        print(f"✅ Retrieved {len(retrieved_docs)} documents")
        for doc in retrieved_docs:
            print(" -", doc.metadata.get("company_id"), "| Chunk:", doc.metadata.get("chunk_id"))

        retrieved_docs.sort(key=lambda d: d.metadata.get("sequence", 0))

        return [
            {"text": doc.page_content, "source": f"{doc.metadata.get('company_id')} | Chunk: {doc.metadata.get('chunk_id')}"}
            for doc in retrieved_docs[:k]
        ]

    except Exception as e:
        print(f"❌ Retrieval Error: {str(e)}")
        return []

def estimate_tokens(text):
    return len(text) // 4

def query_llm_groq(final_query, selected_company=None, chat_history=None, numerical_response=None):
    if not _initialized:
        raise RuntimeError("Components not initialized")

    try:
        relevant_docs = retrieve_documents(final_query, selected_company)
        retrieved_text = "\n\n".join([doc["text"] + "..." for doc in relevant_docs]) if relevant_docs else ""

        sql_context = f"SQL result: {numerical_response}\n\n" if numerical_response else ""
        full_context = sql_context + "Context from documents:\n" + retrieved_text

        history_messages = []
        if chat_history:
            for msg in chat_history[-5:]:
                role = "assistant" if msg['sender'] == 'bot' else "user"
                history_messages.append({"role": role, "content": msg['message']})

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a financial AI assistant that answers using:\n"
                    "1. Numerical data (from SQL)\n"
                    "2. Supporting document context (from RAG)\n\n"
                    "Prioritize the SQL result if it directly answers the question. Use documents for support or elaboration."
                )
            }
        ] + history_messages + [{
            "role": "user",
            "content": f"{full_context}\n\nMy question: {final_query}"
        }]

        total_text = "\n".join([m["content"] for m in messages])
        token_limit = 5800
        if estimate_tokens(total_text) > token_limit:
            excess = estimate_tokens(total_text) - token_limit
            retrieved_text = retrieved_text[: max(len(retrieved_text) - excess * 4, 50)] + "..."
            full_context = sql_context + "Context from documents:\n" + retrieved_text
            messages[-1]["content"] = f"{full_context}\n\nMy question: {final_query}"

        print(f"Estimated tokens: {estimate_tokens(total_text)}")

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="llama3-70b-8192",
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
        sql_answer = input("Enter SQL result if any (or leave blank): ") or None
        answer, sources = query_llm_groq(query, selected_company=company, numerical_response=sql_answer)

        print("\n💡 Answer:")
        print(answer)

        print("\n📄 Sources:")
        for i, doc in enumerate(sources, 1):
            print(f"{i}. Source: {doc['source']}")
            print(f"    Text Preview: {doc['text'][:120]}...\n")
