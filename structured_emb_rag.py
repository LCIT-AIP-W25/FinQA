import os
import time
import re
import json
import faiss
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

# Load environment variables
load_dotenv()

# Configuration
FAISS_STORE_PATH = "p_faiss_store"
DATA_DIR = "./extracted_sec_text"
EMBEDDED_FILES_PATH ="P_embed_faiss.txt" # "embedded_files_faiss.txt"
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')

# --------------------------- Helper Functions ---------------------------
def load_embedded_files():
    """Load already processed files"""
    if os.path.exists(EMBEDDED_FILES_PATH):
        with open(EMBEDDED_FILES_PATH, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_embedded_files(new_files):
    """Update embedded files tracking"""
    existing = load_embedded_files()
    updated = existing.union(set(new_files))
    with open(EMBEDDED_FILES_PATH, "w") as f:
        f.write("\n".join(updated))

def save_faiss_index(vectorstore):
    """Save FAISS index"""
    vectorstore.save_local(FAISS_STORE_PATH)
    print("💾 Vector store updated")

def load_faiss_index():
    """Load existing FAISS index"""
    if os.path.exists(FAISS_STORE_PATH):
        try:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            return FAISS.load_local(FAISS_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            print(f"⚠️ Error loading index: {e}")
    return None

# --------------------------- Enhanced Preprocessing ---------------------------
def financial_preprocessor(text):
    """Clean financial text by removing HTML tags and URLs."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()

# --------------------------- Optimized Chunking ---------------------------
def financial_chunking(text):
    """Hybrid chunking strategy"""
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in ["balance sheet", "income statement", "cash flow"]):
        return 1024  # Structured financial statements
    if len(re.findall(r'\$\d+', text)) > 3:
        return 768   # Dense numerical data
    return 512  # General text

# --------------------------- Draft Embedding Helpers ---------------------------
def save_draft_embedding(file_identifier, texts, metadatas):
    """Save the incomplete embedding as a draft in the 'draft_embedding' folder."""
    folder = "draft_embedding"
    if not os.path.exists(folder):
        os.makedirs(folder)
    base_name = os.path.basename(file_identifier)
    draft_file = os.path.join(folder, base_name + ".draft.json")
    data = {
        "texts": texts,
        "metadatas": metadatas,
        "timestamp": time.time()
    }
    with open(draft_file, "w") as f:
        json.dump(data, f)
    print(f"Draft embedding saved to {draft_file}")

def process_draft_embeddings(session):
    """Attempt to re-embed drafts from the 'draft_embedding' folder."""
    folder = "draft_embedding"
    if not os.path.exists(folder):
        print("No draft embeddings available.")
        return
    draft_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".draft.json")]
    if not draft_files:
        print("No draft embeddings available.")
        return
    for draft_file in draft_files:
        with open(draft_file, "r") as f:
            data = json.load(f)
        print(f"\nProcessing draft embedding from {draft_file}...")
        success = rapid_embedding(session["vectors"], data["texts"], data["metadatas"], file_identifier=draft_file)
        if success:
            print(f"Draft embedding from {draft_file} successfully embedded. Removing draft file.")
            os.remove(draft_file)
        else:
            print(f"Draft embedding from {draft_file} still failing.")

# --------------------------- Rapid Embedding Function ---------------------------
def rapid_embedding(vectorstore, texts, metadatas, file_identifier=None, max_retries=10, max_wait=300):
    """
    Attempts to add the provided texts and metadatas to the vectorstore.
    Retries if a rate limit error (429) is encountered, using exponential backoff capped at max_wait seconds.
    If exceeded, saves the texts and metadatas as a draft embedding.
    
    Returns True if successful, otherwise returns False.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            vectorstore.add_texts(texts, metadatas=metadatas)
            return True
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RATE_LIMIT_EXCEEDED" in error_str:
                wait_time = (2 ** attempt) * 5  # 5, 10, 20, ...
                if wait_time > max_wait:
                    print(f"Wait time {wait_time} seconds exceeds maximum threshold of {max_wait} seconds. Skipping file embedding.")
                    if file_identifier:
                        save_draft_embedding(file_identifier, texts, metadatas)
                    return False
                print(f"Rate limit exceeded, waiting {wait_time} seconds before retrying... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                attempt += 1
            else:
                print(f"Error in rapid_embedding: {e}")
                return False
    if file_identifier:
        save_draft_embedding(file_identifier, texts, metadatas)
    return False

# --------------------------- Sequential File Processing ---------------------------
def process_files_sequentially(session, new_files):
    """Process files with cooling period, error handling, and draft embedding saving.
       Returns a summary with counts and list of skipped files.
    """
    embedded_files = load_embedded_files()
    embedded_count = 0
    skipped_files = []

    for idx, file_path in enumerate(new_files):
        if file_path in embedded_files:
            continue

        print(f"\n🔨 Processing: {os.path.basename(file_path)}")
        start_time = time.time()

        try:
            loader = TextLoader(file_path)
            doc = loader.load()[0]
            doc.page_content = financial_preprocessor(doc.page_content)
            
            chunk_size = financial_chunking(doc.page_content)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=int(chunk_size * 0.2),
                separators=["\n\n", "\n", r"(?<=\. )", " "]
            )
            
            chunks = text_splitter.split_documents([doc])
            if chunks:
                success = rapid_embedding(
                    session["vectors"], 
                    [c.page_content for c in chunks],
                    [c.metadata for c in chunks],
                    file_identifier=file_path
                )
                
                if success:
                    print(f"✅ Embedded {len(chunks)} chunks in {time.time()-start_time:.2f}s")
                    embedded_files.add(file_path)
                    save_embedded_files([file_path])
                    embedded_count += 1
                else:
                    print(f"❌ Skipping {file_path} due to excessive rate limiting.")
                    skipped_files.append(file_path)
                
                if idx < len(new_files)-1:
                    print("⏳ Cooling period: 10s")
                    time.sleep(10)
        except Exception as e:
            print(f"❌ Failed to process {file_path}: {str(e)}")
            with open("processing_errors.log", "a") as f:
                f.write(f"{file_path}: {str(e)}\n")
            skipped_files.append(file_path)

    return {
        "total_files": len(new_files),
        "embedded_count": embedded_count,
        "skipped_files": skipped_files
    }

# --------------------------- Main Workflow ---------------------------
def vector_embedding(session):
    """Core embedding logic with error handling and reporting."""
    existing_vectors = load_faiss_index()
    session["embeddings"] = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    if existing_vectors:
        session["vectors"] = existing_vectors
        print("🔄 Checking for new files...")
        try:
            loader = DirectoryLoader(DATA_DIR, loader_cls=TextLoader)
            current_files = {doc.metadata["source"] for doc in loader.load()}
            new_files = [f for f in current_files if f not in load_embedded_files()]

            if new_files:
                print(f"Found {len(new_files)} new files to process")
                results = process_files_sequentially(session, new_files)
                save_faiss_index(session["vectors"])

                print("\n-------------------------------------")
                print(f"Count of data: {results['total_files']}")
                print(f"Total files embedded: {results['embedded_count']}")
                print(f"Skipped files: {results['skipped_files']}")
                print("-------------------------------------")

                if results["skipped_files"]:
                    retry = input("Do you want to try embedding the skipped files? (y/n): ").lower()
                    if retry == "y":
                        process_files_sequentially(session, results["skipped_files"])
                        save_faiss_index(session["vectors"])
            else:
                print("✅ All files already embedded")
        except Exception as e:
            print(f"❌ Error loading directory: {str(e)}")
    else:
        print("🆕 Creating new vector store...")
        try:
            loader = DirectoryLoader(DATA_DIR, loader_cls=TextLoader)
            docs = loader.load()

            processed_docs = []
            for doc in docs:
                doc.page_content = financial_preprocessor(doc.page_content)
                processed_docs.append(doc)

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=512,
                chunk_overlap=128,
                separators=["\n\n", "\n", r"(?<=\. )", " "]
            )
            chunks = text_splitter.split_documents(processed_docs)

            session["vectors"] = FAISS.from_documents(chunks, session["embeddings"])
            save_faiss_index(session["vectors"])
            save_embedded_files([doc.metadata["source"] for doc in chunks])
        except Exception as e:
            print(f"❌ Initial embedding failed: {str(e)}")
            raise

# --------------------------- Q&A System ---------------------------
def main():
    session = {}
    print("🔍 FinQA - Financial RAG System")
    
    llm = ChatGroq(
        groq_api_key=os.getenv('GROQ_API_KEY'),
        model_name="mixtral-8x7b-32768",
        temperature=0.1
    )

    prompt = ChatPromptTemplate.from_template(
        """Analyze the financial context and provide a precise answer:
<context>
{context}
</context>
Question: {input}
Answer in clear financial terms:"""
    )

    user_choice = input("Initialize embedding process? (y/n): ").lower()
    if user_choice == "y":
        try:
            vector_embedding(session)
        except Exception as e:
            print(f"❌ Critical error during embedding: {str(e)}")
            return
    else:
        session["vectors"] = load_faiss_index()
        if not session["vectors"]:
            print("❌ No vector store available")
            return

    if input("Do you want to try processing draft embeddings? (y/n): ").lower() == "y":
        process_draft_embeddings(session)

    while True:
        try:
            query = input("\nEnter financial question (exit to quit): ").strip()
            if query.lower() in ['exit', 'quit']:
                break

            retrieval_chain = create_retrieval_chain(
                session["vectors"].as_retriever(search_kwargs={"k": 4}),
                create_stuff_documents_chain(llm, prompt)
            )

            start_time = time.time()
            response = retrieval_chain.invoke({"input": query})
            
            print(f"\n⏱️ Response Time: {time.time()-start_time:.2f}s")
            print(f"💡 Answer: {response['answer']}")
            
            if input("Show relevant sources? (y/n): ").lower() == "y":
                print("\n📄 Supporting Documentation:")
                for i, doc in enumerate(response["context"], 1):
                    print(f"\n🔍 Source {i} ({doc.metadata.get('source', 'unknown')}):")
                    content = doc.page_content
                    if len(content) > 400:
                        print(content[:400].strip() + "...")
                    else:
                        print(content)
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Error processing query: {str(e)}")

if __name__ == "__main__":
    main()
