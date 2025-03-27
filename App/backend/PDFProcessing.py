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
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Load environment variables
load_dotenv()

class FinancialRAGSystem:
    def __init__(self):
        # Configuration
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        
        # Initialize components
        self.embeddings = SentenceTransformerEmbeddings(
            model_name="multi-qa-mpnet-base-cos-v1"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", "(?<=\. )", " ", ""]
        )
        self.vector_store = None
        self.groq_client = None
        self.index_name = "financial_reports_faiss_index"
        
        # Initialize Groq client
        self._initialize_groq()

    def _initialize_groq(self):
        """Initialize Groq connection"""
        try:
            self.groq_client = Groq(api_key=self.GROQ_API_KEY)
            print("✅ Groq client initialized successfully")
        except Exception as e:
            print(f"❌ Groq initialization failed: {e}")
            raise

    def _extract_financial_tables(self, page, page_num: int, pdf_path: str) -> List[Document]:
        """Extract and format tables from PDF page"""
        table_docs = []
        tables = page.find_tables()
        
        if tables.tables:
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
                except Exception as e:
                    print(f"Error processing table on page {page_num+1}: {e}")
        return table_docs

    def _is_financial_table(self, df: pd.DataFrame) -> bool:
        """Check if table contains financial data"""
        cols = "|".join(df.columns.astype(str))
        patterns = r"year|quarter|q\d|fy\d|usd|million|billion|revenue|income|balance|assets|liabilities"
        return bool(re.search(patterns, cols, re.IGNORECASE))

    def _format_table(self, df: pd.DataFrame) -> str:
        """Convert table to structured string format"""
        df = df.map(lambda x: re.sub(r"\((\d+)\)", r"-\1", str(x)))
        return df.to_markdown(index=False, floatfmt=".2f")

    def _detect_section(self, text: str) -> str:
        """Detect financial report section"""
        text = text.lower()
        if "balance sheet" in text:
            return "balance_sheet"
        elif "income statement" in text:
            return "income_statement"
        elif "cash flow" in text:
            return "cash_flow"
        return "other"

    def process_pdf(self, pdf_path: str, company_name: str) -> bool:
        """Process PDF file and store in FAISS index"""
        try:
            doc = fitz.open(pdf_path)
            all_docs = []

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)

                # Extract text and tables
                text = page.get_text("text")
                tables = self._extract_financial_tables(page, page_num, pdf_path)

                # Chunk text content
                text_chunks = self.text_splitter.split_text(text)
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

            # ✅ Ensure FAISS index exists before loading
            faiss_index_path = os.path.join(self.index_name, "index.faiss")
            if os.path.exists(self.index_name) and os.path.isfile(faiss_index_path):
                print("✅ Loading existing FAISS index")
                existing_store = FAISS.load_local(
                    self.index_name, self.embeddings, allow_dangerous_deserialization=True
                )
                existing_store.add_documents(all_docs)
                existing_store.save_local(self.index_name)
            else:
                print("⚠ FAISS index missing. Creating a new index...")
                FAISS.from_documents(all_docs, self.embeddings).save_local(self.index_name)

            print(f"✅ Processed {len(all_docs)} chunks from {pdf_path}")
            return True

        except Exception as e:
            print(f"❌ PDF processing failed: {e}")
            return False


    def query_financial_data(self, query: str, company: Optional[str] = None, k: int = 4) -> Tuple[str, List[dict]]:
        """Query the financial data using RAG pipeline"""
        try:
            faiss_index_path = os.path.join(self.index_name, "index.faiss")

            # ✅ Check if FAISS index exists before querying
            if not os.path.exists(self.index_name) or not os.path.isfile(faiss_index_path):
                return "No FAISS index found. Please upload and process a PDF first.", []

            vector_store = FAISS.load_local(
                self.index_name,
                self.embeddings,
                allow_dangerous_deserialization=True
            )

            # Retrieve relevant documents with optional company filter
            if company:
                retrieved_docs = []
                for doc in vector_store.similarity_search(query, k=k*2):  # Fetch extra to filter
                    if doc.metadata.get("company", "").lower() == company.lower():
                        retrieved_docs.append(doc)
                        if len(retrieved_docs) >= k:
                            break
            else:
                retrieved_docs = vector_store.similarity_search(query, k=k)

            if not retrieved_docs:
                return "No relevant documents found.", []

            # Format context for LLM
            context = "\n\n".join([
                f"SOURCE: {doc.metadata.get('source', 'Unknown')} (Page {doc.metadata.get('page', '?')})\n"
                f"SECTION: {doc.metadata.get('section', 'unknown').upper()}\n"
                f"CONTENT:\n{doc.page_content[:1000]}..."
                for doc in retrieved_docs
            ])

            # Query Groq API
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

            # Format sources
            sources = [{
                "content": doc.page_content[:500] + "...",
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "section": doc.metadata.get("section", "unknown").upper(),
                "company": doc.metadata.get("company", "unknown")
            } for doc in retrieved_docs]

            return response.choices[0].message.content, sources

        except Exception as e:
            return f"Error processing query: {str(e)}", []


# Example Usage
if __name__ == "__main__":
    # Initialize system
    rag_system = FinancialRAGSystem()
    
    # Process a PDF (do this once per document)
    rag_system.process_pdf("amazon-annual-report.pdf", "AMZN")
    
    # Query the system
    while True:
        query = input("\nEnter your financial query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
        
        company_filter = input("Filter by company (leave blank for all): ").strip()
        response, sources = rag_system.query_financial_data(
            query, 
            company_filter if company_filter else None
        )
        
        print("\nRESPONSE:")
        print(response)
        
        print("\nSOURCES:")
        for i, source in enumerate(sources, 1):
            print(f"\nSource {i}:")
            print(f"Company: {source['company']}")
            print(f"Document: {source['source']} (Page {source['page']})")
            print(f"Section: {source['section']}")
            print("-" * 50)
            print(source['content'])
            print("-" * 50)