import os
import re
import fitz
import pandas as pd
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import time
from groq_wrapper import GroqWrapper
from pymongo import MongoClient
from typing import List, Tuple
import numpy as np

# Load environment variables
load_dotenv()

class FinancialRAGSystem:
    def __init__(self):
        self.mongo_client = MongoClient(os.getenv("MONGO_URI"))
        self.mongo_db = self.mongo_client["Financial_Rag_DB"]
        self.mongo_collection = self.mongo_db["finqa_pdf"]

        # Configuration
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        
        # Initialize components with enhanced logging
        print("\n=== INITIALIZING FINANCIAL RAG SYSTEM ===")
        self._initialize_embeddings()
        self._initialize_text_splitter()
        self.vector_store = None
        self.index_name = "financial_reports_faiss_index"
        
        # Initialize Groq client through wrapper
        self._initialize_groq()

    def _initialize_embeddings(self):
        """Initialize Google embeddings with validation"""
        print("\n[1/3] Initializing embeddings...")
        try:
            if not self.GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=self.GOOGLE_API_KEY
            )
            
            # Test the embeddings
            test_text = "Financial report analysis"
            start_time = time.time()
            embedding = self.embeddings.embed_query(test_text)
            latency = (time.time() - start_time) * 1000
            
            print(f"✅ Google embeddings initialized successfully")
            print(f"   - Model: models/embedding-001")
            print(f"   - Embedding dimension: {len(embedding)}")
            print(f"   - First 5 values: {embedding[:5]}")
            print(f"   - Latency: {latency:.2f}ms")
            
        except Exception as e:
            print(f"❌ Failed to initialize embeddings: {e}")
            raise

    def _initialize_text_splitter(self):
        """Initialize text splitter with logging"""
        print("\n[2/3] Initializing text splitter...")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            #separators=["\n\n", "\n", "(?<=\. )", " ", ""]
            separators = ["\n\n", "\n", r"(?<=\. )", " ", ""]

        )
        print("✅ Text splitter configured with:")
        print(f"   - Chunk size: 1000")
        print(f"   - Overlap: 200")
        print(f"   - Separators: ['\\n\\n', '\\n', r'(?<=\\. )', ' ', '']")

    def _initialize_groq(self):
        """Initialize Groq connection through wrapper with enhanced logging"""
        print("\n[3/3] Initializing Groq client...")
        try:
            print("   Using GroqWrapper for API key management")
            print("✅ Groq client will be initialized per-request through wrapper")
        except Exception as e:
            print(f"❌ Groq initialization failed: {e}")
            raise

    def _extract_financial_tables(self, page, page_num: int, pdf_path: str) -> List[Document]:
        """Extract and format tables from PDF page with logging"""
        print(f"  Processing page {page_num+1} for tables...")
        table_docs = []
        tables = page.find_tables()
        
        if tables.tables:
            print(f"  Found {len(tables.tables)} tables on page {page_num+1}")
            for i, table in enumerate(tables.tables):
                try:
                    df = table.to_pandas()
                    if not df.empty and self._is_financial_table(df):
                        table_str = self._format_table(df)
                        table_docs.append(Document(
                            page_content=f"TABLE {i+1} FROM PAGE {page_num+1}:\n{table_str}",
                            metadata={
                                "source": pdf_path,
                                "page": page_num + 1,
                                "table_id": i + 1,
                                "type": "financial_table",
                                "section": self._detect_section(page.get_text("text"))
                            }
                        ))
                        print(f"    Added table {i+1} (shape: {df.shape})")
                except Exception as e:
                    print(f"    ❌ Error processing table {i+1}: {e}")
        else:
            print(f"  No tables found on page {page_num+1}")
        return table_docs

    def _is_financial_table(self, df: pd.DataFrame) -> bool:
        """Check if table contains financial data with logging"""
        cols = "|".join(df.columns.astype(str))
        patterns = r"year|quarter|q\d|fy\d|usd|million|billion|revenue|income|balance|assets|liabilities"
        is_financial = bool(re.search(patterns, cols, re.IGNORECASE))
        if not is_financial:
            print(f"    Table filtered out (non-financial): {df.columns.tolist()}")
        return is_financial

    def _format_table(self, df: pd.DataFrame) -> str:
        """Convert table to structured string format"""
        df = df.map(lambda x: re.sub(r"\((\d+)\)", r"-\1", str(x)))
        return df.to_markdown(index=False, floatfmt=".2f")

    def _detect_section(self, text: str) -> str:
        """Detect financial report section with logging"""
        text = text.lower()
        if "balance sheet" in text:
            return "balance_sheet"
        elif "income statement" in text:
            return "income_statement"
        elif "cash flow" in text:
            return "cash_flow"
        return "other"

    def process_pdf(self, pdf_path: str, user_id: str) -> bool:
        """Process PDF file and store embeddings in MongoDB (user-specific, no company)"""
        print(f"\n=== PROCESSING PDF: {pdf_path} ===")
        print(f"User: {user_id}")

        try:
            filename = os.path.basename(pdf_path)
            doc = fitz.open(pdf_path)
            all_chunks = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                #page = doc[page_num]
                text = page.get_text("text")
                section = self._detect_section(text)

                # 1. Process text chunks
                text_chunks = self.text_splitter.split_text(text)
                for i, chunk in enumerate(text_chunks):
                    all_chunks.append({
                        "user_id": str(user_id),
                        "filename": filename,
                        "content": chunk,
                        "metadata": {
                            "page": page_num + 1,
                            "section": section,
                            "type": "text",
                            "chunk_id": i
                        }
                    })

                # 2. Process financial tables
                tables = self._extract_financial_tables(page, page_num, pdf_path)
                for table_doc in tables:
                    all_chunks.append({
                        "user_id": str(user_id),
                        "filename": filename,
                        "content": table_doc.page_content,
                        "metadata": table_doc.metadata
                    })

            print(f"Total text/table chunks: {len(all_chunks)}")
            if not all_chunks:
                print("❌ No valid content extracted.")
                return False

            # 3. Generate embeddings
            texts = [chunk["content"] for chunk in all_chunks]
            embeddings = self.embeddings.embed_documents(texts)

            # 4. Prepare MongoDB docs
            documents = []
            for chunk, embedding in zip(all_chunks, embeddings):
                documents.append({
                    "user_id": str(chunk["user_id"]),
                    "filename": chunk["filename"],
                    "content": chunk["content"],
                    "metadata": chunk["metadata"],
                    "embedding": embedding
                })

            # 5. Remove previous entries
            deleted = self.mongo_collection.delete_many({
                "user_id": str(user_id),
                "filename": filename
            })
            print(f"🧹 Deleted {deleted.deleted_count} old records")

            # 6. Insert fresh records
            inserted = self.mongo_collection.insert_many(documents)
            print(f"✅ Inserted {len(inserted.inserted_ids)} new documents")

            # 7. Delete uploaded PDF
            doc.close()
            os.remove(pdf_path)
            print(f"🗑️ Deleted PDF: {pdf_path}")

            return True

        except Exception as e:
            print(f"❌ PDF processing failed: {e}")
            return False

    def query_financial_data(self, query: str, user_id: str, filename: str, k: int = 4) -> Tuple[str, List[dict]]:
        """Query user-specific PDF data using MongoDB Atlas Vector Search"""
        print(f"\n=== QUERY PROCESSING ===")
        print(f"User: {user_id} | File: {filename} | Question: {query}")
        print(f"Top-K results requested: {k}")

        try:
            start_time = time.time()

            # 1. Generate query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Safe conversion
            query_embedding = np.array(query_embedding).astype(float).tolist()
            print("✅ Generated embedding for query")

            # 2. Run vector search in MongoDB
            print("🔍 Performing vector search in MongoDB Atlas...")
            print(f"Filter: user_id={str(user_id)}, filename={filename}") 
            results = self.mongo_collection.aggregate([
                {
                    "$vectorSearch": {
                        "queryVector": query_embedding,
                        "path": "embedding",
                        "numCandidates": 100,
                        "limit": k,
                        "index": "vector_pdf", 
                        "filter": {
                            "user_id": str(user_id),
                            "filename": filename
                        }
                    }
                }
            ])
            results = list(results)
            print(f"Query vector length: {len(query_embedding)}")
            print(f"First few vector values: {query_embedding[:5]}")

            if not results:
                print("⚠️ No relevant documents found.")
                return "No relevant documents found.", []

            # 3. Prepare LLM context
            print("Preparing context for Groq...")
            context = "\n\n".join([
                f"Page {doc.get('metadata', {}).get('page', '?')} | Section: {doc.get('metadata', {}).get('section', 'unknown').upper()}\n{doc['content'][:1000]}..."
                for doc in results
            ])
            print(f"Total context length: {len(context)} characters")

            # 4. Send to Groq LLM
            print("Sending context and question to Groq LLM...")
            response, error = GroqWrapper.make_rag_request(
                #model="mistral-saba-24b",
                model= "llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a financial analyst. Follow these rules:
    1. Base answers ONLY on the provided context
    2. For numerical questions, provide exact figures with units
    3. For tables, reference the page number
    4. Be concise but complete"""
                    },
                    {
                        "role": "user",
                        "content": f"Context:\n{context}\n\nQuestion: {query}"
                    }
                ],
                temperature=0.3,
                max_tokens=1024
            )

            if error:
                raise Exception(error)

            print("✅ Groq LLM response received")

            # 5. Extract sources
            # sources = [{
            #     "content": doc["content"][:500] + "...",
            #     "source": doc["filename"],
            #     "page": doc.get("metadata", {}).get("page"),
            #     "section": doc.get("metadata", {}).get("section", "unknown").upper()
            # } for doc in results]
            sources = [{
                "content": doc.get("content", "")[:500] + "...",
                "source": doc.get("metadata", {}).get("source", "unknown"),
                "page": doc.get("metadata", {}).get("page", "?"),
                "section": doc.get("metadata", {}).get("section", "unknown").upper()
            } for doc in results]



            print(f"\n=== QUERY COMPLETE ({len(results)} chunks) ===")
            print(f"Total processing time: {time.time() - start_time:.2f} seconds")

            return response.choices[0].message.content, sources

        except Exception as e:
            print(f"\n=== QUERY FAILED ===")
            print(f"❌ Error: {e}")
            return f"Error processing query: {str(e)}", []
        
# Example Usage
if __name__ == "__main__":
    # Initialize system
    print("=== FINANCIAL RAG SYSTEM STARTING ===")
    rag_system = FinancialRAGSystem()