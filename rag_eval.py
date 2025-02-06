import os
import time
import logging
import pandas as pd
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
CSV_FILE_PATH = "new_questions_answers.csv"  # Path to your CSV file

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

def process_questions(session, df):
    """
    Process each question in the DataFrame using the RAG system.
    Save the RAG-generated answers and time taken to the DataFrame.
    """
    # Load LLM from Groq API
    groq_api_key = os.getenv('GROQ_API_KEY')
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
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
    
    # Initialize columns for RAG answers and time taken
    df['RAG Answer'] = None
    df['Time Taken (sec)'] = None

    # Process each question
    for index, row in df.iterrows():
        question = row['Question']
        logger.info(f"Processing Question {index + 1}: {question}")
        
        # Create the retrieval chain
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = session["vectors"].as_retriever()
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Measure time taken
        start_time = time.process_time()
        response = retrieval_chain.invoke({'input': question})
        elapsed_time = time.process_time() - start_time
        
        # Save the RAG answer and time taken to the DataFrame
        df.at[index, 'RAG Answer'] = response['answer']
        df.at[index, 'Time Taken (sec)'] = elapsed_time
        
        logger.info(f"✅ Processed Question {index + 1} in {elapsed_time:.4f} sec")
    
    return df

def main():
    # Use a simple dictionary to mimic session state
    session = {}
    
    logger.info("🔍 FinQA - Financial RAG System")
    
    # Load the CSV file into a DataFrame
    if not os.path.exists(CSV_FILE_PATH):
        logger.error(f"⚠️ CSV file not found at {CSV_FILE_PATH}. Exiting...")
        return
    
    df = pd.read_csv(CSV_FILE_PATH)
    logger.info(f"✅ Loaded CSV file with {len(df)} questions.")
    
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

    # Process all questions in the DataFrame
    df = process_questions(session, df)
    
    # Save the updated DataFrame to a new CSV file
    output_csv_path = "questions_with_rag_answers.csv"
    df.to_csv(output_csv_path, index=False)
    logger.info(f"✅ Saved RAG answers and time taken to {output_csv_path}")

if __name__ == "__main__":
    main()