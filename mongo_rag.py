import os
import time
import re
import urllib.parse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.schema import Document, BaseRetriever

# Load environment variables
load_dotenv()

# Configuration
# CHANGE THIS: Update DATA_DIR to match the path where your extracted_sec_text_test folder is located on your system
DATA_DIR = "./extracted_sec_text_test"
METADATA_FILE = "embedded_files.txt"
# Get the URI from .env and parse it to encode username/password
raw_uri = os.getenv('MONGODB_URI')
if not raw_uri:
    raise ValueError("MONGODB_URI must be set in .env file for MongoDB Atlas connection")

# Parse the URI to extract and encode username/password
uri_parts = urllib.parse.urlparse(raw_uri)
username = urllib.parse.quote_plus(uri_parts.username)  # Encode username
password = urllib.parse.quote_plus(uri_parts.password)  # Encode password

# Reconstruct the URI with encoded credentials
encoded_uri = urllib.parse.urlunparse(
    (uri_parts.scheme, f"{username}:{password}@{uri_parts.hostname}", uri_parts.path, uri_parts.params, uri_parts.query, uri_parts.fragment)
)

DB_NAME = "financial_db"
COLLECTION_NAME = "financial_chunks"
HTML_CLEANER = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
REFERENCE_PATTERN = re.compile(r'\[\d+\]|\(Source:.*?\)')

# MongoDB setup with encoded URI
client = MongoClient(encoded_uri)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Test MongoDB connection
try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
except Exception as e:
    print(f"❌ MongoDB Atlas connection failed: {str(e)}")
    raise

# Helper Functions
def load_embedded_files():
    """Load already processed files from metadata file."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return set(line.strip() for line in f if line.strip())
    return set()

def save_embedded_file(file_path):
    """Append a new embedded file path to the metadata file."""
    with open(METADATA_FILE, "a") as f:
        f.write(f"{file_path}\n")

def financial_preprocessor(text):
    """Clean financial text by removing HTML tags and URLs."""
    text = BeautifulSoup(text, "html.parser").get_text()
    text = URL_PATTERN.sub('', text)
    return text.strip()

def financial_chunking(text):
    """Hybrid chunking strategy."""
    text = text.lower()
    if any(keyword in text for keyword in ["balance sheet", "income statement", "cash flow"]):
        return 1024
    if len(re.findall(r'\$\d+', text)) > 3:
        return 768
    return 512

def rapid_embedding(texts, metadatas, embeddings, max_retries=3, max_wait=300):
    """Embed texts and insert into MongoDB with retry logic for rate limits and MongoDB errors."""
    attempt = 0
    while attempt < max_retries:
        try:
            embeddings_list = embeddings.embed_documents(texts)
            documents = [
                {"text": text, "metadata": metadata, "embedding": embedding}
                for text, metadata, embedding in zip(texts, metadatas, embeddings_list)
            ]
            collection.insert_many(documents)
            return True
        except pymongo.errors.ConnectionFailure as e:
            print(f"❌ MongoDB Atlas connection error: {str(e)}")
            return False  # Skip the file instead of waiting (adjust as needed)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RATE_LIMIT_EXCEEDED" in error_str:
                wait_time = (2 ** attempt) * 5
                if wait_time > max_wait:
                    print(f"Wait time {wait_time}s exceeds max {max_wait}s. Skipping embedding.")
                    return False
                print(f"Rate limit hit, waiting {wait_time}s (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
                attempt += 1
            else:
                print(f"Error in rapid_embedding: {str(e)}")
                return False
    return False

def process_files_sequentially(embeddings, new_files):
    """Process files and embed into MongoDB, checking metadata file."""
    embedded_files = load_embedded_files()
    embedded_count = 0
    skipped_files = []

    for idx, file_path in enumerate(new_files):
        if file_path in embedded_files:
            print(f"⏩ Skipping {os.path.basename(file_path)} (already embedded)")
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
                    [c.page_content for c in chunks],
                    [c.metadata for c in chunks],
                    embeddings
                )
                if success:
                    print(f"✅ Embedded {len(chunks)} chunks in {time.time()-start_time:.2f}s")
                    save_embedded_file(file_path)
                    embedded_count += 1
                else:
                    print(f"❌ Skipping {file_path} due to rate limiting or connection error.")
                    skipped_files.append(file_path)
                
                if idx < len(new_files) - 1:
                    print("⏳ Cooling period: 90s")
                    time.sleep(90)
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

def vector_embedding():
    """Embed new files into MongoDB."""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    loader = DirectoryLoader(DATA_DIR, loader_cls=TextLoader)
    current_files = [doc.metadata["source"] for doc in loader.load()]
    
    results = process_files_sequentially(embeddings, current_files)
    print("\n-------------------------------------")
    print(f"Count of data: {results['total_files']}")
    print(f"Total files embedded: {results['embedded_count']}")
    print(f"Skipped files: {results['skipped_files']}")
    print("-------------------------------------")
    if results["skipped_files"] and input("Retry skipped files? (y/n): ").lower() == "y":
        process_files_sequentially(embeddings, results["skipped_files"])

class MongoDBRetriever(BaseRetriever):
    def __init__(self, collection, embeddings, k=4):
        self.collection = collection
        self.embeddings = embeddings
        self.k = k
    
    def get_relevant_documents(self, query):
        """Retrieve top-k documents via vector search (requires Atlas Search index)."""
        query_embedding = self.embeddings.embed_query(query)
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    # CHANGE THIS: Ensure "vector_index" matches the name of your vector search index in MongoDB Atlas
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "limit": self.k,
                    "numCandidates": 100
                }
            },
            {
                "$project": {
                    "text": 1,
                    "metadata": 1,
                    "score": {"$meta": "vectorSearchScore"}
                }
            }
        ]
        results = list(self.collection.aggregate(pipeline))
        return [Document(page_content=r["text"], metadata=r["metadata"]) for r in results]

def main():
    print("🔍 FinQA - Financial RAG System")
    
    llm = ChatGroq(
        groq_api_key=os.getenv('GROQ_API_KEY'),
        # CHANGE THIS: Ensure GROQ_API_KEY in your .env file is correct for your Groq API access
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

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # CHANGE THIS: Ensure you have Google Generative AI API access configured (API key or credentials in .env)
    
    user_choice = input("Initialize embedding process? (y/n): ").lower()
    if user_choice == "y":
        try:
            vector_embedding()
        except Exception as e:
            print(f"❌ Critical error during embedding: {str(e)}")
            return
    
    retriever = MongoDBRetriever(collection, embeddings, k=4)
    
    while True:
        try:
            query = input("\nEnter financial question (exit to quit): ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            
            retrieval_chain = create_retrieval_chain(
                retriever,
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
                    print(doc.page_content[:400].strip() + "..." if len(doc.page_content) > 400 else doc.page_content)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Error processing query: {str(e)}")

if __name__ == "__main__":
    main()