import os
import time
import logging
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables from .env file
load_dotenv()

# Define file paths for FAISS persistence and data directory
DATA_DIR = "./data"

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and a stream handler
file_handler = logging.FileHandler('finqa.log')
stream_handler = logging.StreamHandler()

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def save_faiss_index(faiss_vectorstore):
    """Save the full FAISS vector database (index + docstore) to disk."""
    faiss_vectorstore.save_local("faiss_store")
    logger.info("✅ FAISS vector store saved successfully.")

def load_faiss_index():
    """Load the full FAISS vector database (index + docstore) from disk."""
    if os.path.exists("faiss_store"):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Recreate embeddings
            faiss_vectorstore = FAISS.load_local("faiss_store", embeddings, allow_dangerous_deserialization=True)
            logger.info("✅ Loaded FAISS index from disk. Skipping re-embedding.")
            return faiss_vectorstore
        except Exception as e:
            logger.error("⚠️ Error loading FAISS index: %s", e)
    return None

def vector_embedding(session):
    """
    Creates and stores vector embeddings only if not already stored.
    The embeddings are generated in batches to respect Google API limits.
    """
    if "vectors" not in session:
        # Try loading existing FAISS index
        stored_vectors = load_faiss_index()
        if stored_vectors:
            session["vectors"] = stored_vectors
            return  # Skip re-embedding

        # Initialize embeddings and load documents
        session["embeddings"] = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        session["loader"] = DirectoryLoader(DATA_DIR, glob="*.txt", loader_cls=TextLoader)
        session["docs"] = session["loader"].load()
        session["text_splitter"] = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        session["final_documents"] = session["text_splitter"].split_documents(session["docs"])

        # Batch embedding process
        batch_size = 5  # Google AI supports only 5 texts per request in most regions
        final_documents_texts = [doc.page_content for doc in session["final_documents"]]
        
        # Split texts into batches
        batched_texts = [
            final_documents_texts[i:i + batch_size]
            for i in range(0, len(final_documents_texts), batch_size)
        ]
        
        embedded_vectors = []
        for batch in batched_texts:
            try:
                # Embed in small batches to respect API limits
                embeddings_batch = session["embeddings"].embed_documents(batch)
                embedded_vectors.extend(embeddings_batch)
                time.sleep(1)  # Pause to prevent hitting request limits
            except Exception as e:
                logger.error("Error embedding batch: %s", e)
        
        # Now create FAISS index using the full list of document texts
        session["vectors"] = FAISS.from_texts(final_documents_texts, session["embeddings"])
        
        # Save FAISS index for future use
        save_faiss_index(session["vectors"])
        logger.info("✅ Vector Store DB is Ready & Persisted.")

def main():
    # Use a simple dictionary to mimic session state
    session = {}
    
    logger.info("🔍 FinQA - Financial RAG System")
    
    # Load API Keys from environment variables
    groq_api_key = os.getenv('GROQ_API_KEY')
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    
    # Load LLM from Groq API
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")
    
    # Define the structured prompt template
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the questions based on the provided context only.
        Provide the most accurate response.
        <context>
        {context}
        <context>
        Question: {input}
        """
    )
    
    # Ask the user whether to generate and store embeddings
    user_input = input("Generate & Store Embeddings? (y/n): ").strip().lower()
    if user_input == "y":
        vector_embedding(session)
    else:
        # Attempt to load the existing FAISS index
        vectors = load_faiss_index()
        if vectors:
            session["vectors"] = vectors
        else:
            logger.info("No stored vector database found. Generating embeddings now...")
            vector_embedding(session)
    
    # Display stored embeddings details if available
    if "vectors" in session:
        logger.info("\nFAISS Index Details:")
        logger.info(session["vectors"].index)
        logger.info("✅ Number of stored vectors: %s", session["vectors"].index.ntotal)
    else:
        logger.info("No vectors available. Exiting...")
        return

    # Get user input for query
    prompt_input = input("\nEnter Your Question from Stored Documents: ").strip()
    if prompt_input and "vectors" in session:
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = session["vectors"].as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
        start = time.process_time()
        response = retrieval_chain.invoke({'input': prompt_input})
        elapsed_time = time.process_time() - start
        logger.info(f"\n⏳ Response Time: {elapsed_time:.4f} sec")
        
        # Print the answer
        print("\nAnswer:")
        print(response['answer'])
        
        # Ask the user if they want to see the similarity search results
        show_similarity = input("\nDo you want to see the similarity search results? (y/n): ").strip().lower()
        if show_similarity == "y":
            logger.info("\n📂 Document Similarity Search:")
            for doc in response["context"]:
                logger.info(doc.page_content)
                logger.info("--------------------------------")
    else:
        logger.info("No query entered. Exiting...")

if __name__ == "__main__":
    main()