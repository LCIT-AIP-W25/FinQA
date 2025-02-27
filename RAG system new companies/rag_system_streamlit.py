import os
import json
import faiss
import numpy as np
import re
import streamlit as st
import tempfile
import pandas as pd
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from groq import Groq
from rouge_score import rouge_scorer
from bert_score import score as bert_score
from tqdm import tqdm
from sklearn.metrics import f1_score

# ✅ Load API Keys from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GROQ_API_KEY or not GOOGLE_API_KEY:
    raise ValueError("❌ Missing API Keys. Please set GROQ_API_KEY and GOOGLE_API_KEY in .env file.")

# ✅ Set Google API Key for Embeddings
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ✅ Define File Paths
FAISS_INDEX_DIR = r"C:\Users\AutomaC\Desktop\AIP\RAG system new companies\Streamlit app"
DOCUMENT_PATH = r"C:\Users\AutomaC\Desktop\AIP\RAG system new companies\Streamlit app\combined_document.txt"

# Create directory if it doesn't exist
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# Verify document exists
if not os.path.exists(DOCUMENT_PATH):
    raise FileNotFoundError(f"❌ Document not found at {DOCUMENT_PATH}")

# ✅ 1️⃣ Chunking Functions
def split_by_headings(text):
    """Split document by headings (H1, H2, etc.)."""
    chunks = re.split(r"\n\s*(?=[A-Z][A-Za-z ]{3,}\n)", text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]

def recursive_chunking(chunks, chunk_size=1000, chunk_overlap=200):
    """Apply recursive chunking after heading-based split."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    refined_chunks = []
    for chunk in chunks:
        refined_chunks.extend(text_splitter.split_text(chunk))
    return refined_chunks

# ✅ 2️⃣ FAISS Index Handling
def load_faiss_index():
    """Load FAISS index or create new one"""
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    try:
        st.info("✅ Loading FAISS index...")
        return FAISS.load_local(
            FAISS_INDEX_DIR,
            embedding_model,
            allow_dangerous_deserialization=True
        ).as_retriever()
    except Exception as e:
        st.warning(f"⚠️ Index loading failed: {e}. Generating new index...")
        return generate_faiss_index()

def generate_faiss_index():
    """Generate and save new FAISS index"""
    try:
        with st.spinner("🔄 Processing document..."):
            # Load and chunk document
            with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
                document_text = f.read()
            
            heading_chunks = split_by_headings(document_text)
            final_chunks = recursive_chunking(heading_chunks)
            docs = [Document(page_content=chunk) for chunk in final_chunks]

            # Create and save index
            embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            vector_db = FAISS.from_documents(docs, embedding_model)
            vector_db.save_local(FAISS_INDEX_DIR)
            
            st.success("✅ New FAISS index created successfully!")
            return vector_db.as_retriever()

    except Exception as e:
        st.error(f"❌ Critical error during index creation: {e}")
        return None

# ✅ 3️⃣ Evaluation Metrics
def calculate_metrics(generated_answer, reference_answer):
    """Calculate evaluation metrics between generated and reference answers"""
    metrics = {}
    
    # ROUGE Scores
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'])
    rouge_scores = rouge.score(reference_answer, generated_answer)
    for key in rouge_scores:
        metrics[key] = rouge_scores[key].fmeasure
    
    # BERTScore
    P, R, F1 = bert_score([generated_answer], [reference_answer], lang="en")
    metrics['bert_precision'] = P.mean().item()
    metrics['bert_recall'] = R.mean().item()
    metrics['bert_f1'] = F1.mean().item()
    
    # Token-level F1
    generated_tokens = set(generated_answer.split())
    reference_tokens = set(reference_answer.split())
    
    tp = len(generated_tokens & reference_tokens)
    fp = len(generated_tokens - reference_tokens)
    fn = len(reference_tokens - generated_tokens)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    metrics['token_f1'] = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return metrics

# ✅ 4️⃣ Query Handling
def query_llm_groq(question, reference_answer=None, _retriever=None):
    """Handle query processing with external retriever"""
    try:
        # Use cached retriever if provided
        retriever = _retriever if _retriever else load_faiss_index()
        relevant_docs = retriever.get_relevant_documents(question)
        retrieved_text = "\n\n".join([doc.page_content for doc in relevant_docs])

        client = Groq(api_key=GROQ_API_KEY)
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{
                "role": "user",
                "content": f"You are an AI assistant specializing in business analysis. Given a company's annual report, financial statements, or other business-related documents. Use this context and answer the question in brief covering all the aspects:\n{retrieved_text}\n\nAnswer this: {question}"
            }],
            temperature=0.3,
            max_tokens=128
        )
        
        generated_answer = response.choices[0].message.content
        result = {
            "answer": generated_answer,
            "retrieved_context": retrieved_text
        }
        
        if reference_answer:
            result["metrics"] = calculate_metrics(generated_answer, reference_answer)
            
        return result
        
    except Exception as e:
        return {"error": f"❌ Error processing query: {str(e)}"}

# ✅ 5️⃣ Streamlit UI
st.title("📊 Financial Analysis Assistant with Evaluation")
st.write("Powered by FAISS and Mistral LLM")

# Mode selection
mode = st.radio("Select Mode:", ["Single Query", "Batch Evaluation"])

if mode == "Single Query":
    user_question = st.text_input("💬 Ask your financial question:")
    reference_answer = st.text_area("🔏 Reference Answer (for evaluation):")
    
    if st.button("🔍 Analyze"):
        if user_question:
            with st.spinner("🔍 Analyzing..."):
                try:
                    result = query_llm_groq(user_question, reference_answer)
                    
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.success("✅ Analysis Complete!")
                        
                        # Display answers
                        with st.expander("💡 Generated Answer"):
                            st.write(result["answer"])
                        
                        if reference_answer:
                            st.subheader("📈 Evaluation Metrics")
                            metrics = result["metrics"]
                            
                            # Metric columns
                            cols = st.columns(3)
                            cols[0].metric("ROUGE-L F1", f"{metrics['rougeL']:.2f}")
                            cols[1].metric("BERT F1", f"{metrics['bert_f1']:.2f}")
                            cols[2].metric("Token F1", f"{metrics['token_f1']:.2f}")
                            
                            # Detailed metrics
                            with st.expander("📊 Detailed Metrics"):
                                st.write("### ROUGE Scores")
                                st.json({
                                    "ROUGE-1": f"{metrics['rouge1']:.2f}",
                                    "ROUGE-2": f"{metrics['rouge2']:.2f}",
                                    "ROUGE-L": f"{metrics['rougeL']:.2f}"
                                })
                                
                                st.write("### BERT Scores")
                                st.json({
                                    "Precision": f"{metrics['bert_precision']:.2f}",
                                    "Recall": f"{metrics['bert_recall']:.2f}",
                                    "F1": f"{metrics['bert_f1']:.2f}"
                                })
                except Exception as e:
                    st.error(f"❌ Analysis failed: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question first")

else:  # Batch Evaluation Mode
    uploaded_file = st.file_uploader("Upload evaluation CSV:", type=["csv"])
    if uploaded_file:
        try:
            # Load index once at start
            with st.spinner("🔍 Loading FAISS index..."):
                batch_retriever = load_faiss_index()
            
            if batch_retriever is None:
                st.error("Failed to load FAISS index. Cannot proceed with batch processing.")
            else:
                df = pd.read_csv(uploaded_file)
                if 'question' not in df.columns or 'reference_answer' not in df.columns:
                    st.error("CSV must contain 'question' and 'reference_answer' columns")
                else:
                    full_results = []
                    progress_bar = st.progress(0)
                    
                    # Process all rows with pre-loaded retriever
                    for i, row in tqdm(df.iterrows(), total=len(df)):
                        result = query_llm_groq(
                            row['question'], 
                            row['reference_answer'],
                            _retriever=batch_retriever
                        )
                        full_results.append({
                            "question": row['question'],
                            "reference": row['reference_answer'],
                            "generated": result.get("answer", ""),
                            "metrics": result.get("metrics", {})
                        })
                        progress_bar.progress((i+1)/len(df))
                
                # Display results
                if full_results:
                    # Create results dataframe
                    results_df = pd.DataFrame([{
                        'Question': res['question'],
                        'Reference Answer': res['reference'],
                        'Generated Answer': res['generated'],
                        'ROUGE-L': res['metrics'].get('rougeL', 0),
                        'BERT F1': res['metrics'].get('bert_f1', 0),
                        'Token F1': res['metrics'].get('token_f1', 0)
                    } for res in full_results])
                    
                    # Show answers
                    with st.expander("📄 View All Q&A Pairs"):
                        for idx, res in enumerate(full_results, 1):
                            st.markdown(f"### Pair {idx}")
                            st.write(f"**Question:** {res['question']}")
                            st.write(f"**Reference Answer:** {res['reference']}")
                            st.write(f"**Generated Answer:** {res['generated']}")
                            st.write("---")
                    
                    # Download button
                    csv = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Full Results",
                        data=csv,
                        file_name='rag_evaluation.csv',
                        mime='text/csv'
                    )
                    
                    # Aggregate metrics
                    avg_metrics = {
                        'rougeL': np.mean([res['metrics'].get('rougeL', 0) for res in full_results]),
                        'bert_f1': np.mean([res['metrics'].get('bert_f1', 0) for res in full_results]),
                        'token_f1': np.mean([res['metrics'].get('token_f1', 0) for res in full_results])
                    }
                    
                    st.subheader("📊 Aggregate Metrics")
                    cols = st.columns(3)
                    cols[0].metric("Avg ROUGE-L", f"{avg_metrics['rougeL']:.2f}")
                    cols[1].metric("Avg BERT F1", f"{avg_metrics['bert_f1']:.2f}")
                    cols[2].metric("Avg Token F1", f"{avg_metrics['token_f1']:.2f}")
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

# ✅ Index Management
st.sidebar.header("Index Management")
if st.sidebar.button("🔄 Rebuild Index"):
    with st.spinner("Rebuilding index..."):
        generate_faiss_index()
    st.sidebar.success("Index rebuilt successfully!")

if st.sidebar.button("🧹 Clear Index"):
    if os.path.exists(FAISS_INDEX_DIR):
        for f in os.listdir(FAISS_INDEX_DIR):
            os.remove(os.path.join(FAISS_INDEX_DIR, f))
        os.rmdir(FAISS_INDEX_DIR)
    st.sidebar.success("Index cleared!")