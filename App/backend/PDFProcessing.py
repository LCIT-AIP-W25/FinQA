import os
import re
import fitz
import pandas as pd
from dotenv import load_dotenv
from typing import List, Tuple, Optional
from langchain.schema import Document
from langchain_groq import ChatGroq
from groq import Groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import time

# Load environment variables
load_dotenv()

class FinancialRAGSystem:
    def __init__(self):
        # Configuration
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        
        # Initialize components with enhanced logging
        print("\n=== INITIALIZING FINANCIAL RAG SYSTEM ===")
        self._initialize_embeddings()
        self._initialize_text_splitter()
        self.vector_store = None
        self.groq_client = None
        self.index_name = "financial_reports_faiss_index"
        
        # Initialize Groq client
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
            separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )
        print("✅ Text splitter configured with:")
        print(f"   - Chunk size: 1000")
        print(f"   - Overlap: 200")
        print(f"   - Separators: ['\\n\\n', '\\n', '(?<=\\. )', ' ', '']")

    def _initialize_groq(self):
        """Initialize Groq connection with enhanced logging"""
        print("\n[3/3] Initializing Groq client...")
        try:
            if not self.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            
            self.groq_client = Groq(api_key=self.GROQ_API_KEY)
            print("✅ Groq client initialized successfully")
            print(f"   - API Key: {self.GROQ_API_KEY[:5]}...{self.GROQ_API_KEY[-5:]}")
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

    def process_pdf(self, pdf_path: str, company_name: str) -> bool:
        """Process PDF file and store in FAISS index with comprehensive logging"""
        print(f"\n=== PROCESSING PDF: {pdf_path} ===")
        print(f"Company: {company_name}")
        
        try:
            start_time = time.time()
            doc = fitz.open(pdf_path)
            all_docs = []
            total_pages = len(doc)
            
            print(f"Document has {total_pages} pages")
            
            for page_num in range(total_pages):
                page = doc.load_page(page_num)
                print(f"\nProcessing page {page_num+1}/{total_pages}...")

                # Extract text and tables
                text = page.get_text("text")
                tables = self._extract_financial_tables(page, page_num, pdf_path)

                # Chunk text content
                text_chunks = self.text_splitter.split_text(text)
                print(f"  Split into {len(text_chunks)} text chunks")
                
                for i, chunk in enumerate(text_chunks):
                    all_docs.append(Document(
                        page_content=chunk,
                        metadata={
                            "type": "text",
                            "section": self._detect_section(chunk),
                            "chunk_id": i,
                            "company": company_name,
                            "source": pdf_path,
                            "page": page_num + 1
                        }
                    ))

                # Add tables
                all_docs.extend(tables)
                print(f"  Total documents after page {page_num+1}: {len(all_docs)}")

            # Handle FAISS index
            faiss_index_path = os.path.join(self.index_name, "index.faiss")
            processing_time = time.time() - start_time
            
            if os.path.exists(self.index_name) and os.path.isfile(faiss_index_path):
                print("\nLoading existing FAISS index...")
                existing_store = FAISS.load_local(
                    self.index_name, self.embeddings, allow_dangerous_deserialization=True
                )
                print(f"  Adding {len(all_docs)} new documents to index")
                existing_store.add_documents(all_docs)
                existing_store.save_local(self.index_name)
                print("✅ Updated existing FAISS index")
            else:
                print("\nCreating new FAISS index...")
                FAISS.from_documents(all_docs, self.embeddings).save_local(self.index_name)
                print("✅ Created new FAISS index")

            print(f"\n=== PROCESSING COMPLETE ===")
            print(f"Total processing time: {processing_time:.2f} seconds")
            print(f"Total documents processed: {len(all_docs)}")
            print(f"Index location: {self.index_name}")
            return True

        except Exception as e:
            print(f"\n=== PROCESSING FAILED ===")
            print(f"Error: {e}")
            return False

    def query_financial_data(self, query: str, company: Optional[str] = None, k: int = 4) -> Tuple[str, List[dict]]:
        """Query the financial data using RAG pipeline with detailed logging"""
        print(f"\n=== QUERY PROCESSING ===")
        print(f"Query: {query}")
        print(f"Company filter: {company if company else 'None'}")
        print(f"Requested documents: {k}")
        
        try:
            start_time = time.time()
            faiss_index_path = os.path.join(self.index_name, "index.faiss")

            # Check FAISS index existence
            if not os.path.exists(self.index_name) or not os.path.isfile(faiss_index_path):
                print("❌ No FAISS index found")
                return "No FAISS index found. Please upload and process a PDF first.", []

            print("Loading FAISS index...")
            load_start = time.time()
            vector_store = FAISS.load_local(
                self.index_name,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print(f"  Index loaded in {(time.time() - load_start):.2f}s")

            # Retrieve relevant documents
            print("\nExecuting similarity search...")
            search_start = time.time()
            
            if company:
                print(f"  Applying company filter for: {company}")
                retrieved_docs = []
                for doc in vector_store.similarity_search(query, k=k*2):  # Fetch extra to filter
                    if doc.metadata.get("company", "").lower() == company.lower():
                        retrieved_docs.append(doc)
                        if len(retrieved_docs) >= k:
                            break
                print(f"  Found {len(retrieved_docs)} matching documents after filtering")
            else:
                retrieved_docs = vector_store.similarity_search(query, k=k)
                print(f"  Found {len(retrieved_docs)} documents")

            if not retrieved_docs:
                print("⚠️ No relevant documents found")
                return "No relevant documents found.", []

            # Log retrieved documents
            print("\nRetrieved documents:")
            for i, doc in enumerate(retrieved_docs, 1):
                print(f"  {i}. {doc.metadata.get('source', 'Unknown')}")
                print(f"     Page: {doc.metadata.get('page', '?')}")
                print(f"     Section: {doc.metadata.get('section', 'unknown').upper()}")
                print(f"     Type: {doc.metadata.get('type', 'unknown')}")
                print(f"     Company: {doc.metadata.get('company', 'unknown')}")
                print(f"     Content preview: {doc.page_content[:100]}...\n")

            # Prepare LLM context
            print("Preparing LLM context...")
            context = "\n\n".join([
                f"SOURCE: {doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', '?')})\n"
                f"SECTION: {doc.metadata.get('section', 'unknown').upper()}\n"
                f"CONTENT:\n{doc.page_content[:1000]}..."
                for doc in retrieved_docs
            ])
            print(f"  Context length: {len(context)} characters")

            # Query Groq API
            print("\nQuerying Groq API...")
            llm_start = time.time()
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
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
            print(f"  LLM response received in {(time.time() - llm_start):.2f}s")

            # Prepare sources
            sources = [{
                "content": doc.page_content[:500] + "...",
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "section": doc.metadata.get("section", "unknown").upper(),
                "company": doc.metadata.get("company", "unknown")
            } for doc in retrieved_docs]

            total_time = time.time() - start_time
            print(f"\n=== QUERY COMPLETE ===")
            print(f"Total processing time: {total_time:.2f} seconds")
            
            return response.choices[0].message.content, sources

        except Exception as e:
            print(f"\n=== QUERY FAILED ===")
            print(f"Error: {e}")
            return f"Error processing query: {str(e)}", []


# Example Usage
if __name__ == "__main__":
    # Initialize system
    print("=== FINANCIAL RAG SYSTEM STARTING ===")
    rag_system = FinancialRAGSystem()
    
    