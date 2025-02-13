import os
import time
import re
import faiss
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, TokenTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables
load_dotenv()

# Define constants
FAISS_STORE_PATH = "faiss_store_new_chunk"
DATA_DIR = "./data2"
EMBEDDED_FILES_PATH = "embedded_files.txt"  # File to track already embedded file sources

# --------------------------- Helper Functions for Tracking Embedded Files ---------------------------

def load_embedded_files():
    """Load the set of file sources that have already been embedded."""
    if os.path.exists(EMBEDDED_FILES_PATH):
        with open(EMBEDDED_FILES_PATH, "r") as f:
            files = set(line.strip() for line in f if line.strip())
        return files
    return set()

def save_embedded_files(embedded_files):
    """Save the set of file sources to disk."""
    with open(EMBEDDED_FILES_PATH, "w") as f:
        for file in embedded_files:
            f.write(file + "\n")

# --------------------------- FAISS Vector Database Handling ---------------------------

def save_faiss_index(faiss_vectorstore):
    """Save FAISS vector database to disk."""
    faiss_vectorstore.save_local(FAISS_STORE_PATH)
    print("✅ FAISS vector store saved successfully.")

def load_faiss_index():
    """Load FAISS vector database from disk if available."""
    if os.path.exists(FAISS_STORE_PATH):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            faiss_vectorstore = FAISS.load_local(FAISS_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
            print("✅ Loaded FAISS index from disk.")
            return faiss_vectorstore
        except Exception as e:
            print(f"⚠️ Error loading FAISS index: {e}")
    return None

# --------------------------- Dynamic Chunking Strategy ---------------------------

def get_dynamic_chunk_size(text):
    """
    Adjusts chunk size dynamically based on content type.
    """
    if any(keyword in text.lower() for keyword in ["balance sheet", "cash flow", "income statement", "net sales"]):
        return 1200  # Larger chunks for structured financial data
    elif len(text) < 800:
        return 700   # Smaller chunks for dense financial narrative
    else:
        return 900   # Default for general text

def get_text_splitter(mode="character", sample_text=""):
    """
    Returns a text splitter based on the chosen mode.
    """
    if mode == "token":
        return TokenTextSplitter(chunk_size=512, chunk_overlap=64)
    chunk_size = get_dynamic_chunk_size(sample_text)
    chunk_overlap = min(150, chunk_size // 2)
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )

# --------------------------- Batch Processing for Embedding ---------------------------

def add_texts_in_batches(vectorstore, texts, metadatas, batch_size=10, delay=2):
    """
    Add texts to the vector store in smaller batches to avoid hitting rate limits.
    :param vectorstore: The FAISS vector store.
    :param texts: List of text chunks to embed.
    :param metadatas: Corresponding metadata for each text chunk.
    :param batch_size: Number of texts to process per batch.
    :param delay: Delay in seconds between batches.
    """
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        batch_metadatas = metadatas[i:i+batch_size]
        vectorstore.add_texts(batch_texts, metadatas=batch_metadatas)
        print(f"Embedded batch {i // batch_size + 1}")
        time.sleep(delay)

# --------------------------- Update Embeddings for New Files ---------------------------

def update_embeddings(session, splitter_mode="character"):
    """
    Check for new files in DATA_DIR that are not already embedded,
    and add their embeddings to the existing FAISS vector store.
    """
    # Load the list of embedded file sources
    embedded_files = load_embedded_files()
    
    # Load documents from the data folder
    loader = DirectoryLoader(DATA_DIR, glob="*.txt", loader_cls=TextLoader)
    docs = loader.load()
    if not docs:
        print("No documents found in the data directory.")
        return

    # Ensure each document has a 'source' in metadata (set by DirectoryLoader)
    for doc in docs:
        if "source" not in doc.metadata or not doc.metadata["source"]:
            doc.metadata["source"] = doc.metadata.get("file_path", "unknown")

    # Filter out docs that have already been embedded
    new_docs = [doc for doc in docs if doc.metadata.get("source") not in embedded_files]
    if not new_docs:
        print("No new files to embed. All files are already embedded.")
        return

    print(f"Found {len(new_docs)} new file(s) to embed.")

    # Use sample text from the first new document for dynamic chunk sizing
    sample_text = new_docs[0].page_content if new_docs else ""
    text_splitter = get_text_splitter(mode=splitter_mode, sample_text=sample_text)
    new_documents = text_splitter.split_documents(new_docs)

    new_texts = [doc.page_content for doc in new_documents]
    new_metadatas = [doc.metadata for doc in new_documents]

    # Add new texts in batches to avoid rate limiting
    add_texts_in_batches(session["vectors"], new_texts, new_metadatas, batch_size=10, delay=2)
    print(f"Embedded {len(new_docs)} new file(s) and added them to the vector store.")

    # Update the embedded files record
    for doc in new_docs:
        embedded_files.add(doc.metadata.get("source"))
    save_embedded_files(embedded_files)
    save_faiss_index(session["vectors"])

# --------------------------- Embedding & Vector Storage ---------------------------

def vector_embedding(session, splitter_mode="character"):
    """
    Creates and stores vector embeddings.
    If a FAISS index exists, update it with new files.
    Otherwise, create a new index from scratch.
    """
    existing_vectors = load_faiss_index()
    session["embeddings"] = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    if existing_vectors:
        session["vectors"] = existing_vectors
        print("Updating existing FAISS index with any new files...")
        update_embeddings(session, splitter_mode=splitter_mode)
    else:
        print("No existing FAISS index found. Generating new embeddings...")
        loader = DirectoryLoader(DATA_DIR, glob="*.txt", loader_cls=TextLoader)
        docs = loader.load()
        if not docs:
            print("No documents found in the data directory.")
            return

        # Ensure each document has a 'source' in metadata
        for doc in docs:
            if "source" not in doc.metadata or not doc.metadata["source"]:
                doc.metadata["source"] = doc.metadata.get("file_path", "unknown")

        sample_text = docs[0].page_content if docs else ""
        text_splitter = get_text_splitter(mode=splitter_mode, sample_text=sample_text)
        final_documents = text_splitter.split_documents(docs)

        final_texts = [doc.page_content for doc in final_documents]
        final_metadatas = [doc.metadata for doc in final_documents]

        session["vectors"] = FAISS.from_texts(final_texts, session["embeddings"], metadatas=final_metadatas)
        save_faiss_index(session["vectors"])
        print("✅ Vector Store DB is Ready & Persisted.")

        # Save all embedded file sources
        all_sources = set(doc.metadata.get("source") for doc in docs if doc.metadata.get("source"))
        save_embedded_files(all_sources)

# --------------------------- Financial Number Extraction ---------------------------

def extract_financial_figure(text):
    """Extracts numerical values from financial responses."""
    match = re.search(r"\$\d{1,3}(?:,\d{3})*(?:\.\d+)?\s?(?:billion|million)?", text, re.IGNORECASE)
    return match.group(0) if match else None

# --------------------------- Main Function ---------------------------

def main():
    session = {}
    print("🔍 FinQA - Financial RAG System")
    
    # Load API Keys
    groq_api_key = os.getenv('GROQ_API_KEY')
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    # Initialize LLM
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")

    # Prompt template
    prompt = ChatPromptTemplate.from_template(
        """Answer based on context only:
        <context>
        {context}
        </context>
        Question: {input}"""
    )

    # User Input: Generate & Store or Update Embeddings
    user_input = input("Generate & Store Embeddings? (y/n): ").strip().lower()
    if user_input == "y":
        vector_embedding(session)
    else:
        vectors = load_faiss_index()
        if vectors:
            session["vectors"] = vectors
            # Optionally update embeddings with new files
            update_embeddings(session)
        else:
            print("No existing vector store found. Generating new embeddings...")
            vector_embedding(session)

    # Loop for Question & Answer sessions
    while True:
        prompt_input = input("\nEnter Your Question (or type 'exit' to quit): ").strip()
        if prompt_input.lower() == "exit":
            break

        if "vectors" in session and session["vectors"]:
            document_chain = create_stuff_documents_chain(llm, prompt)
            retriever = session["vectors"].as_retriever()
            retrieval_chain = create_retrieval_chain(retriever, document_chain)

            start = time.process_time()
            response = retrieval_chain.invoke({'input': prompt_input})
            elapsed_time = time.process_time() - start

            financial_value = extract_financial_figure(response['answer'])

            print(f"\n⏳ Response Time: {elapsed_time:.4f} sec")
            if financial_value:
                print(f"\n💡 Answer (Extracted Data): {financial_value}")
            else:
                print("\n💡 Answer:", response['answer'])

            show_similarity = input("\nShow similarity results? (y/n): ").strip().lower()
            if show_similarity == 'y':
                print("\n📄 Relevant Document Chunks:")
                for i, doc in enumerate(response["context"], 1):
                    print(f"\n🔍 Chunk {i}:")
                    print(doc.page_content)
                    print("―――――――――――――――――――――――――――――――――――")
        else:
            print("❌ Vector store not available. Exiting...")
            break

if __name__ == "__main__":
    main()
