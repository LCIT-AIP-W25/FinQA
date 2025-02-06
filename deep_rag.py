import os
import time
import numpy as np
import faiss
import pandas as pd
from langchain_huggingface import HuggingFaceEmbeddings
import ollama
from string import Template
from nltk.tokenize import sent_tokenize
import nltk
from rouge_score import rouge_scorer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from bert_score import score as bert_score
from nltk.translate.bleu_score import sentence_bleu

# Ensure nltk dependencies are available
nltk.download('punkt')

# Load embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
eval_embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")  # For cosine similarity

def load_document(filepath):
    """Load the content of the unique document file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()

def semantic_chunking(text, max_chunk_size=512):
    """Chunk text into smaller, meaningful semantic chunks based on sentences."""
    sentences = sent_tokenize(text)
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) > max_chunk_size:
            chunks.append(chunk.strip())
            chunk = ""
        chunk += sentence + " "
    if chunk:
        chunks.append(chunk.strip())  # Add last chunk if non-empty
    return chunks

# Load and chunk the document
document_path = r'C:\Users\AutomaC\Desktop\AIP\FinQ&A\unique_documents.txt'
document_content = load_document(document_path)
document_chunks = semantic_chunking(document_content)

# Generate embeddings for document chunks
document_embeddings = embeddings.embed_documents(document_chunks)
document_embeddings = np.array(document_embeddings).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(document_embeddings.shape[1])
index.add(document_embeddings)  # Add document embeddings to the index

class SimpleRetriever:
    """Simple FAISS-based retriever class."""
    def __init__(self, index, embeddings, chunks):
        self.index = index
        self.embeddings = embeddings
        self.chunks = chunks
    
    def retrieve(self, query, k=3):
        query_embedding = self.embeddings.embed_query(query)
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]

retriever = SimpleRetriever(index, embeddings, document_chunks)

# Craft the prompt template
prompt_template = Template("""
Use ONLY the context below.
If unsure, say "I don't know".
Keep answers under 4 sentences.

Context: $context
Question: $question
Answer:
""")

def answer_query(question, retriever):
    """Retrieve context, generate an answer, and measure response time."""
    start_time = time.time()  # Start response timer

    # Retrieve relevant context
    context = retriever.retrieve(question)
    combined_context = "\n".join(context)

    response = ollama.generate(
        model="qwen:1.8b",
        prompt=prompt_template.substitute(context=combined_context, question=question)
    )

    response_time = time.time() - start_time  # End response timer
    return response['response'].strip(), round(response_time, 4)  # Return answer and time taken

def evaluate_answers(generated_answers, reference_answers):
    """Compute evaluation metrics."""
    bleu_scores = []
    rouge_scores = []
    cosine_scores = []
    bert_scores = []

    # Compute BERTScore
    P, R, F1 = bert_score(generated_answers, reference_answers, lang="en", rescale_with_baseline=True)

    for gen, ref, f1 in zip(generated_answers, reference_answers, F1):
        # Compute BLEU score
        bleu = sentence_bleu([ref.split()], gen.split())
        bleu_scores.append(bleu)

        # Compute ROUGE score
        scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        scores = scorer.score(ref, gen)
        rouge_scores.append(scores['rougeL'].fmeasure)

        # Compute cosine similarity
        gen_embedding = eval_embedding_model.encode(gen, convert_to_tensor=True)
        ref_embedding = eval_embedding_model.encode(ref, convert_to_tensor=True)
        cosine_sim = cosine_similarity([gen_embedding.cpu().numpy()], [ref_embedding.cpu().numpy()])[0][0]
        cosine_scores.append(cosine_sim)

        # Store BERT F1-score
        bert_scores.append(f1.item())

    return bleu_scores, rouge_scores, cosine_scores, bert_scores

# Load questions and reference answers from Excel
excel_path = r'C:\Users\AutomaC\Desktop\AIP\FinQ&A\questions_answers.xlsx'
df = pd.read_excel(excel_path)

# Normalize column names (strip spaces and lowercase)
df.columns = df.columns.str.strip()

# Debugging: Print column names
print("Available columns:", df.columns.tolist())

# Check if required columns exist
if 'Question' not in df.columns or 'Answer' not in df.columns:
    raise KeyError(f"Columns 'Question' or 'Answer' not found. Available columns: {df.columns.tolist()}")

# Generate answers using RAG and measure response time
generated_answers = []
response_times = []

for question in df['Question']:
    answer, time_taken = answer_query(question, retriever)
    generated_answers.append(answer)
    response_times.append(time_taken)

df['Generated Answer'] = generated_answers
df['Response Time (s)'] = response_times  # Store response time

# Evaluate the generated answers
bleu_scores, rouge_scores, cosine_scores, bert_scores = evaluate_answers(
    generated_answers,
    df['Answer'].tolist()
)

# Add scores to DataFrame
df['BLEU Score'] = bleu_scores
df['ROUGE-L Score'] = rouge_scores
df['Cosine Similarity'] = cosine_scores
df['BERTScore (F1)'] = bert_scores

# Save results to a new Excel file
output_path = r'C:\Users\AutomaC\Desktop\AIP\FinQ&A\rag_evaluation_results.xlsx'
df.to_excel(output_path, index=False)

print(f"✅ RAG evaluation completed. Results saved to {output_path}")
