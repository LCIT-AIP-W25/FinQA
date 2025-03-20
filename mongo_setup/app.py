import streamlit as st
from ingestion import connect_to_mongo, validate_mongo_connection
from embedding import init_embeddings, validate_embedding_model
from retrieval import init_vector_store, retrieve_documents
from generation import init_groq_llm, generate_answer

# Initialize components
st.title("Financial RAG System")

# Connect to MongoDB
collection = connect_to_mongo()
if not validate_mongo_connection(collection):
    st.error("Failed to connect to MongoDB. Please check your configuration.")
    st.stop()

# Initialize embeddings
embeddings = init_embeddings()
if not validate_embedding_model(embeddings):
    st.error("Failed to initialize embedding model.")
    st.stop()

# Initialize vector store
vector_store = init_vector_store(collection, embeddings)
if not vector_store:
    st.error("Failed to initialize vector store. Ensure the 'st_vector_index' exists in MongoDB Atlas.")
    st.stop()

# Initialize Groq LLM
llm = init_groq_llm()
if not llm:
    st.error("Failed to initialize Groq LLM. Check your API key.")
    st.stop()

# User input
question = st.text_input("Enter your question about financial data:")

if st.button("Submit"):
    if question:
        # Embed the question
        with st.spinner("Processing your question..."):
            # Retrieve relevant documents
            retrieved_docs = retrieve_documents(vector_store, question, k=3)
            if not retrieved_docs:
                st.warning("No relevant documents found.")
            else:
                # Generate answer
                answer = generate_answer(llm, question, retrieved_docs)
                st.success("Answer generated!")
                st.write("**Question:**", question)
                st.write("**Answer:**", answer)
                st.write("**Sources:**")
                for i, doc in enumerate(retrieved_docs):
                    st.write(f"Source {i+1} ({doc.metadata.get('company_id', 'Unknown')}, {doc.metadata.get('chunk_id', 'Unknown')}):")
                    st.write(f"{doc.page_content[:200]}...")
    else:
        st.warning("Please enter a question.")

