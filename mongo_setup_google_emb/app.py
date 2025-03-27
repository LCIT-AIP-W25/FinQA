import os
import re
import streamlit as st
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_groq import ChatGroq
from embedding import init_embeddings, validate_embedding_model

# Load environment variables from .env file
load_dotenv()

# List of distinct company names
DISTINCT_COMPANIES = ['All', 'AMD', 'AT&T', 'Amazon', 'Google', 'JP Morgan', 'Mastercard', 
                      'McDonald', 'Meta', 'Netflix', 'Pepsico', 'S&P Global', 'Tesla']

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
        st.success("✅ Connected to MongoDB Atlas")
        return collection
    except Exception as e:
        st.error(f"❌ MongoDB connection failed: {e}")
        return None

def validate_mongo_connection(collection):
    """Validate the MongoDB connection by checking document count."""
    try:
        count = collection.estimated_document_count()
        st.info(f"✅ MongoDB Collection validated: {count} documents found")
        return True
    except Exception as e:
        st.error(f"❌ MongoDB validation failed: {e}")
        return False

# ------------------- Groq LLM Connection ------------------- #
def connect_to_groq():
    """Connect to Groq LLM using API key from environment."""
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        
        llm = ChatGroq(temperature=0.2, model="mistral-saba-24b", api_key=groq_api_key)
        st.success("✅ Connected to Groq LLM")
        return llm
    except Exception as e:
        st.error(f"❌ Groq LLM connection failed: {e}")
        return None

# ------------------- Vector Store ------------------- #
def init_vector_store(collection):
    """Initialize MongoDB Atlas Vector Search with embeddings."""
    try:
        embeddings = init_embeddings()
        if not validate_embedding_model(embeddings):
            st.error("❌ Embedding model validation failed")
            return None

        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name="st_vector_index",
            embedding_key="embedding",
            text_key="content"
        )
        st.success("✅ Vector store initialized")
        return vector_store
    except Exception as e:
        st.error(f"❌ Vector store initialization failed: {e}")
        return None

# ------------------- Document Retrieval ------------------- #
def extract_quarter_from_question(question):
    """
    Extract the quarter (Q1, Q2, Q3, Q4) mentioned in the question, if any.
    
    Args:
        question: User's query string
    
    Returns:
        Quarter number (1, 2, 3, 4) if found, else None
    """
    quarter_pattern = r'\bQ([1-4])\b'
    match = re.search(quarter_pattern, question, re.IGNORECASE)
    if match:
        return match.group(1)  # Returns '1', '2', '3', or '4'
    return None

def retrieve_documents(vector_store, question, k=3, selected_company=None):
    """
    Retrieve documents from vector store based on a question and optional company filter.
    If a quarter (e.g., Q2) is mentioned in the question, filter by that quarter.
    
    Args:
        vector_store: Initialized MongoDBAtlasVectorSearch instance
        question: User's query string
        k: Number of documents to retrieve (default: 3)
        selected_company: Company name to filter by (default: None)
    
    Returns:
        List of retrieved documents
    """
    filter_query = None
    if selected_company and selected_company != "All":
        if selected_company not in DISTINCT_COMPANIES:
            st.warning(f"⚠️ Warning: '{selected_company}' not in known companies: {DISTINCT_COMPANIES}")
            return []
        
        # Check if a specific quarter is mentioned in the question
        quarter = extract_quarter_from_question(question)
        if quarter:
            # Filter for the specific quarter (e.g., "Amazon_Q1 2023.txt")
            filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}_Q{quarter} \\d{{4}}\\.txt$", "$options": "i"}}
            st.info(f"Quarter {quarter} detected in question. Filter applied: {filter_query}")
        else:
            # Filter for any quarter (Q1 to Q4)
            filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}_Q[1-4] \\d{{4}}\\.txt$", "$options": "i"}}
            st.info(f"No specific quarter detected. Filter applied: {filter_query}")
    
    try:
        # Perform vector search with the filter
        retrieved_docs = vector_store.similarity_search(question, k=k, filter=filter_query)
        
        # Log the initially retrieved documents for debugging
        if retrieved_docs:
            st.info("Initially retrieved documents:")
            for i, doc in enumerate(retrieved_docs):
                st.write(f"Document {i+1} company_id: {doc.metadata.get('company_id', 'Unknown')}")
        
        # Additional check: Ensure only documents from the selected company are returned
        if selected_company and selected_company != "All":
            filtered_docs = [
                doc for doc in retrieved_docs
                if doc.metadata.get("company_id", "").lower().startswith(selected_company.lower())
            ]
            if len(filtered_docs) != len(retrieved_docs):
                st.warning(f"⚠️ Warning: Some retrieved documents did not match the selected company '{selected_company}'. Filtered them out.")
            retrieved_docs = filtered_docs

        if not retrieved_docs and selected_company and selected_company != "All":
            st.warning(f"⚠️ No documents found for company: {selected_company}")
        return retrieved_docs
    except Exception as e:
        st.error(f"❌ Document retrieval failed: {e}")
        return []

# ------------------- Streamlit App ------------------- #
def main():
    st.title("WealthWiz AI Chat")
    st.markdown("Ask financial questions about companies and get AI-powered answers!")

    # Initialize session state for connections
    if "initialized" not in st.session_state:
        # Connect to MongoDB
        collection = connect_to_mongo()
        if collection is None or not validate_mongo_connection(collection):
            st.stop()

        # Connect to Groq LLM
        llm = connect_to_groq()
        if llm is None:
            st.stop()

        # Initialize Vector Store
        vector_store = init_vector_store(collection)
        if vector_store is None:
            st.stop()

        # Store in session state
        st.session_state["llm"] = llm
        st.session_state["vector_store"] = vector_store
        st.session_state["initialized"] = True

    # UI Elements
    selected_company = st.selectbox("Select a Company", DISTINCT_COMPANIES, index=0)  # Default to "All"
    question = st.text_input("Enter your question:", placeholder="e.g., What were Amazon's Q1 2023 financial results?")
    submit_button = st.button("Submit")

    if submit_button and question:
        with st.spinner("Retrieving documents and generating response..."):
            # Retrieve documents
            retrieved_docs = retrieve_documents(
                vector_store=st.session_state["vector_store"],
                question=question,
                k=3,
                selected_company=selected_company
            )

            # Display retrieved documents
            if retrieved_docs:
                st.subheader("Retrieved Documents")
                for i, doc in enumerate(retrieved_docs):
                    st.markdown(f"**Document {i+1}:**")
                    st.write(f"**Content (first 200 chars):** {doc.page_content}...")
                    st.write(f"**Metadata:** {doc.metadata}..")
                    st.markdown("---")
            else:
                st.warning("No relevant documents found.")

            # Generate LLM response if documents are retrieved
            if retrieved_docs:
                context = "\n\n".join([doc.page_content for doc in retrieved_docs])
                prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {question}"
                
                try:
                    response = st.session_state["llm"].invoke(prompt)
                    st.subheader("LLM Response")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"❌ LLM response generation failed: {e}")
            else:
                st.error("Cannot generate a response without retrieved documents.")

if __name__ == "__main__":
    main()# Add error handling for the case when no documents are retrieved
def retrieve_documents(vector_store, question, k=3, selected_company=None):
    """
    Retrieve documents from vector store based on a question and optional company filter.
    If a quarter (e.g., Q2) is mentioned in the question, filter by that quarter.
    
    Args:
        vector_store: Initialized MongoDBAtlasVectorSearch instance
        question: User's query string
        k: Number of documents to retrieve (default: 3)
        selected_company: Company name to filter by (default: None)
    
    Returns:
        List of retrieved documents
    """
    filter_query = None
    if selected_company and selected_company != "All":
        if selected_company not in DISTINCT_COMPANIES:
            st.warning(f"⚠️ Warning: '{selected_company}' not in known companies: {DISTINCT_COMPANIES}")
            return []
        
        # Check if a specific quarter is mentioned in the question
        quarter = extract_quarter_from_question(question)
        if quarter:
            # Filter for the specific quarter (e.g., "Amazon_Q1 2023.txt")
            filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}_Q{quarter} \\d{{4}}\\.txt$", "$options": "i"}}
            st.info(f"Quarter {quarter} detected in question. Filter applied: {filter_query}")
        else:
            # Filter for any quarter (Q1 to Q4)
            filter_query = {"company_id": {"$regex": f"^{re.escape(selected_company)}_Q[1-4] \\d{{4}}\\.txt$", "$options": "i"}}
            st.info(f"No specific quarter detected. Filter applied: {filter_query}")
    
    try:
        # Perform vector search with the filter
        retrieved_docs = vector_store.similarity_search(question, k=k, filter=filter_query)
        
        # Log the initially retrieved documents for debugging
        if retrieved_docs:
            st.info("Initially retrieved documents:")
            for i, doc in enumerate(retrieved_docs):
                st.write(f"Document {i+1} company_id: {doc.metadata.get('company_id', 'Unknown')}")
        
        # Additional check: Ensure only documents from the selected company are returned
        if selected_company and selected_company != "All":
            filtered_docs = [
                doc for doc in retrieved_docs
                if doc.metadata.get("company_id", "").lower().startswith(selected_company.lower())
            ]
            if len(filtered_docs) != len(retrieved_docs):
                st.warning(f"⚠️ Warning: Some retrieved documents did not match the selected company '{selected_company}'. Filtered them out.")
            retrieved_docs = filtered_docs

        if not retrieved_docs and selected_company and selected_company != "All":
            st.warning(f"⚠️ No documents found for company: {selected_company}")
            return []
        elif not retrieved_docs:
            st.warning("⚠️ No documents found for the given question.")
            return []
        return retrieved_docs
    except Exception as e:
        st.error(f"❌ Document retrieval failed: {e}")
        return []

# Improve the main function to handle exceptions and provide better user experience
def main():
    try:
        st.title("WealthWiz AI Chat")
        st.markdown("Ask financial questions about companies and get AI-powered answers!")

        # Initialize session state for connections
        if "initialized" not in st.session_state:
            # Connect to MongoDB
            collection = connect_to_mongo()
            if collection is None or not validate_mongo_connection(collection):
                st.stop()

            # Connect to Groq LLM
            llm = connect_to_groq()
            if llm is None:
                st.stop()

            # Initialize Vector Store
            vector_store = init_vector_store(collection)
            if vector_store is None:
                st.stop()

            # Store in session state
            st.session_state["llm"] = llm
            st.session_state["vector_store"] = vector_store
            st.session_state["initialized"] = True

        # UI Elements
        selected_company = st.selectbox("Select a Company", DISTINCT_COMPANIES, index=0)  # Default to "All"
        question = st.text_input("Enter your question:", placeholder="e.g., What were Amazon's Q1 2023 financial results?")
        submit_button = st.button("Submit")

        if submit_button and question:
            with st.spinner("Retrieving documents and generating response..."):
                # Retrieve documents
                retrieved_docs = retrieve_documents(
                    vector_store=st.session_state["vector_store"],
                    question=question,
                    k=3,
                    selected_company=selected_company
                )

                # Display retrieved documents
                if retrieved_docs:
                    st.subheader("Retrieved Documents")
                    for i, doc in enumerate(retrieved_docs):
                        st.markdown(f"**Document {i+1}:**")
                        st.write(f"**Content (first 200 chars):** {doc.page_content}...")
                        st.write(f"**Metadata:** {doc.metadata}..")
                        st.markdown("---")
                else:
                    st.warning("No relevant documents found.")

                # Generate LLM response if documents are retrieved
                if retrieved_docs:
                    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
                    prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {question}"
                    
                    try:
                        response = st.session_state["llm"].invoke(prompt)
                        st.subheader("LLM Response")
                        st.write(response.content)
                    except Exception as e:
                        st.error(f"❌ LLM response generation failed: {e}")
                else:
                    st.error("Cannot generate a response without retrieved documents.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()