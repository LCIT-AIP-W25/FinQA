import streamlit as st
import re
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from rouge_score import rouge_scorer
from bert_score import score as bert_score
import time
import os
import traceback

# Import from retrieval.py
from retrieval import initialize_components, query_llm_groq, GROQ_API_KEY, MONGO_URI

# Load environment variables
load_dotenv()

# Initialize components from retrieval.py
if not initialize_components():
    st.error("Failed to initialize components. Check MongoDB connection and API keys.")
    st.stop()

def generate_answer(question, company_name):
    """Generate an answer using the RAG system."""
    start_time = time.time()
    answer, _ = query_llm_groq(question, selected_company=company_name)
    response_time = time.time() - start_time
    return answer, response_time

def calculate_metrics(generated_answer, reference_answer):
    """Compute ROUGE, BERTScore, and Token F1 between generated and reference."""
    metrics = {}
    try:
        # ROUGE
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

    except Exception as e:
        st.warning(f"Metric calculation error: {e}")
    return metrics

st.title("🔍 RAG Evaluation System")

uploaded_file = st.file_uploader("Upload Combined CSV", type=["csv"])

# Test vs. Full Mode
run_mode = st.sidebar.selectbox("Run Mode", ["Test (5 rows)", "Full Dataset"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # Validate columns
    required_columns = ['Question', 'reference_answer', 'Document']
    if not all(col in df.columns for col in required_columns):
        st.error("CSV must contain 'Document', 'Question', and 'reference_answer' columns")
    else:
        st.success(f"✅ Loaded {len(df)} questions from CSV")

        if run_mode == "Test (5 rows)":
            df = df.head(5)
            st.info("⚠️ Running in TEST MODE (first 5 rows only)")
        else:
            st.info(f"🟢 Running FULL evaluation on {len(df)} rows")

        if st.button("⚙️ Start Evaluation"):
            start_batch = time.time()
            progress_bar = st.progress(0)
            status_box = st.empty()
            results = []
            errors_encountered = False

            # Timestamped CSV name
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            partial_file = f"partial_results_{timestamp}.csv"
            
            for i, row in df.iterrows():
                row_start_time = time.time()

                try:
                    question = row['Question']
                    reference_answer = row['reference_answer']
                    document_name = row['Document']

                    # Extract company name from Document (e.g., "Amazon" from "Amazon_Q1_2023")
                    company_name = None
                    if isinstance(document_name, str):
                        match = re.match(r"^(.*?)_Q[1-4]", document_name)
                        if match:
                            company_name = match.group(1)

                    # Generate answer
                    generated_answer, response_time = generate_answer(question, company_name)

                    # Calculate metrics
                    metrics = calculate_metrics(generated_answer, reference_answer)

                    # Record timing
                    row_elapsed = round(time.time() - row_start_time, 2)
                    
                    # Build result row
                    result_dict = {
                        'Document': document_name,
                        'Question': question,
                        'Reference': reference_answer,
                        'Generated': generated_answer,
                        'Company': company_name,
                        'TimeTaken(sec)': row_elapsed,
                        'LLM_Response_Time(sec)': response_time,
                    }
                    result_dict.update(metrics)
                    results.append(result_dict)

                except Exception as e:
                    errors_encountered = True
                    st.warning(f"Row {i} failed: {e}")
                    traceback.print_exc()
                
                # Save partial results
                temp_df = pd.DataFrame(results)
                temp_df.to_csv(partial_file, index=False)

                # Update progress and ETA
                avg_time_so_far = np.mean([r['TimeTaken(sec)'] for r in results]) if results else 0
                remaining = len(df) - (i + 1)
                est_remaining_time = remaining * avg_time_so_far

                progress_bar.progress((i + 1) / len(df))
                status_box.info(
                    f"Processed Q{i+1}/{len(df)} | Last Q: {row_elapsed:.2f}s | ETA: {est_remaining_time/60:.2f} min"
                )

            total_batch_time = time.time() - start_batch
            st.success(f"🎉 Evaluation completed in {total_batch_time/60:.2f} min")

            # Convert results to DataFrame
            results_df = pd.DataFrame(results)

            # Display top results
            st.write("### Top 5 Results")
            st.write(results_df.head(5))

            # Aggregate metrics
            if not results_df.empty:
                avg_metrics = {
                    'ROUGE-1': results_df['rouge1'].mean(),
                    'ROUGE-2': results_df['rouge2'].mean(),
                    'ROUGE-L': results_df['rougeL'].mean(),
                    'BERT F1': results_df['bert_f1'].mean(),
                    'Token F1': results_df['token_f1'].mean(),
                    'Avg Time (sec)': results_df['TimeTaken(sec)'].mean(),
                    'LLM Response Avg (sec)': results_df['LLM_Response_Time(sec)'].mean()
                }

                st.subheader("📊 Aggregate Metrics")
                col1, col2, col3 = st.columns(3)
                col1.metric("Avg ROUGE-L", f"{avg_metrics['ROUGE-L']:.2f}")
                col2.metric("Avg BERT F1", f"{avg_metrics['BERT F1']:.2f}")
                col3.metric("Avg Token F1", f"{avg_metrics['Token F1']:.2f}")

                with st.expander("⏱️ Full Metrics"):
                    st.json(avg_metrics)

            # Save final results
            final_file = f"batch_results_{timestamp}.csv"
            results_df.to_csv(final_file, index=False)
            csv_data = results_df.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Results CSV",
                data=csv_data,
                file_name=final_file,
                mime='text/csv'
            )

            if errors_encountered:
                st.warning(f"Some rows had errors. Partial results saved in '{partial_file}'.")
            else:
                st.success("No errors encountered.")