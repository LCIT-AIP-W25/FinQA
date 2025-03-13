import os
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from groq import Groq

# Load environment variables
load_dotenv()

# Configuration
FAISS_STORE_PATH = "Rag"
DATA_DIR = "extracted_sec_text"
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Ensure this is set in your .env file

# --------------------------- Helper Functions ---------------------------

def load_faiss_index():
    """Load the combined FAISS index."""
    if os.path.exists(FAISS_STORE_PATH):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            return FAISS.load_local(FAISS_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            return f"❌ Error loading FAISS index: {e}"
    return None

def financial_preprocessor(text):
    """Remove HTML tags and URLs."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()

def parse_company_name(file_name):
    """Extracts the company name from a file name."""
    base = os.path.basename(file_name)
    match = re.match(r"^(.*?)_", base)
    if match:
        return match.group(1)
    return os.path.splitext(base)[0]

def list_companies():
    """List distinct company names from files in DATA_DIR."""
    companies = set()
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".txt"):
            companies.add(parse_company_name(file_name))
    return sorted(companies)

def retrieve_documents(retriever, query):
    """Retrieve relevant documents along with metadata."""
    try:
        relevant_docs = retriever.get_relevant_documents(query)
        results = []
        for doc in relevant_docs:
            source = doc.metadata.get("source", "Unknown Source")
            text = doc.page_content
            results.append({"text": text, "source": source})
        return results
    except Exception as e:
        return f"❌ Retrieval Error: {str(e)}"

def query_llm_groq(question, retriever):
    """Queries Groq API directly using the provided retriever context."""
    try:
        relevant_docs = retrieve_documents(retriever, question)

        if isinstance(relevant_docs, str):  # Error Handling
            return relevant_docs, []

        retrieved_text = "\n\n".join([doc["text"][:400] + "..." for doc in relevant_docs])

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{
                "role": "user",
                "content": (
                    "You are a financial AI assistant that provides concise answers based on retrieved documents.\n"
                    "Based on the following retrieved information, answer the question:\n\n"
                    f"{retrieved_text}\n\nQuestion: {question}"
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

# --------------------------- RAG API Functions ---------------------------

def handle_contextual_query(user_question):
    """Handles contextual questions using RAG-based retrieval."""
    vector_store = load_faiss_index()
    if vector_store is None or isinstance(vector_store, str):
        return {"error": "Vector store not available. Please run the embedding process first."}, 500

    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    response, relevant_docs = query_llm_groq(user_question, retriever)

    if isinstance(response, str) and response.startswith("❌"):
        return {"error": response}, 500

    sources = [{"source": doc["source"], "snippet": doc["text"][:200]} for doc in relevant_docs]
    return {
        "response": response,
        "sources": sources
    }, 200
