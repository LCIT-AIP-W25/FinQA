import os
import time
import re
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from groq import Groq
 
# Load environment variables
load_dotenv()
 
# Configuration
FAISS_STORE_PATH = r"C:\Users\user\OneDrive - Loyalist College\AIandDS\Term 4\FinQA_Project_Env\React_App\backend\Rag"  # Combined FAISS index location
DATA_DIR = r"C:\Users\user\OneDrive - Loyalist College\AIandDS\Term 4\Github_repo\FinQA\RAG system new companies\extracted_sec_text"
EMBEDDED_FILES_PATH = "P_embed_faiss.txt"
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
            st.error(f"⚠️ Error loading index: {e}")
    return None
 
def financial_preprocessor(text):
    """Remove HTML tags and URLs."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()
 
def parse_company_name(file_name):
    """Extracts the company name from a file name.
       E.g. "Amazon_Q2 2023.txt" -> "Amazon"
    """
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
 
# --------------------------- Streamlit UI ---------------------------
st.title("📊 Financial RAG System")
 
st.sidebar.header("Select Company")
companies = list_companies()
selected_company = st.sidebar.selectbox("📌 Choose a Company", companies)
 
st.header("💡 Ask a Financial Question")
question_input = st.text_input("🔍 Enter your question:")
 
if st.button("Submit Query"):
    if not question_input:
        st.warning("⚠️ Please enter a question.")
    else:
        # Append the selected company to the query.
        final_query = f"[Company: {selected_company}] {question_input}"
        st.write("⏳ Loading vector store...")
 
        vector_store = load_faiss_index()
        if vector_store is None:
            st.error("❌ Vector store not available. Please run the embedding process first.")
        else:
            retriever = vector_store.as_retriever(search_kwargs={"k": 4})
            with st.spinner("🔄 Querying AI Model..."):
                start_time = time.time()
                answer, sources = query_llm_groq(final_query, retriever)
                elapsed = time.time() - start_time
            
            st.markdown(f"⏱ **Response Time:** {elapsed:.2f} seconds")
            st.markdown("🎯 **Answer:**")
            st.write(answer)
            
            if sources:
                if st.checkbox("Show relevant sources"):
                    relevant_docs = retriever.get_relevant_documents(final_query)
                    st.markdown("### Supporting Documentation")
                    for i, doc in enumerate(relevant_docs, 1):
                        with st.expander(f"Source {i}: {doc.metadata.get('source', 'unknown')}"):
                            st.write(doc.page_content)