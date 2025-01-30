import json
import re
from datetime import datetime
import numpy as np
from rank_bm25 import BM25Okapi
from transformers import T5ForConditionalGeneration, T5Tokenizer
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss

# 1. Data Extraction with Temporal Filtering and Chunking
def load_filtered_chunks(file_path, chunk_size=256):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)[:10]  # First 10 entries

    chunks = []
    for entry in data:
        # Temporal filtering (keep 2023+ entries)
        if 'date' in entry and datetime.strptime(entry['date'], "%Y-%m-%d").year < 2023:
            continue
            
        # Extract metadata
        metadata = {
            'filename': entry.get('filename', 'N/A'),
            'id': entry.get('id', 'N/A'),
            'timestamp': entry.get('date', '2023-01-01')
        }

        # Combine and chunk text
        full_text = ' '.join(entry.get('pre_text', [])) + ' ' + ' '.join(entry.get('post_text', []))
        words = full_text.split()
        
        # Simple word-based chunking
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i+chunk_size])
            chunks.append({
                'text': chunk,
                'metadata': metadata
            })
    
    return chunks

# 2. Hybrid Retriever
class HybridRetriever:
    def __init__(self, embedding_model='all-mpnet-base-v2'):
        self.embedding_model = SentenceTransformer(embedding_model)
        self.bm25 = None
        self.faiss_index = None
        self.cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        self.documents = None  # Initialize documents attribute
    
    def index(self, documents):
        # Store documents
        self.documents = documents
        
        # BM25 indexing
        tokenized_docs = [doc['text'].split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
        
        # FAISS indexing
        embeddings = self.embedding_model.encode([doc['text'] for doc in documents], convert_to_tensor=True).cpu().numpy()
        embeddings = np.array(embeddings).astype('float32')
        
        self.faiss_index = faiss.IndexFlatIP(embeddings.shape[1])
        faiss.normalize_L2(embeddings)
        self.faiss_index.add(embeddings)
        
    def search(self, query, top_k=3):
        # Semantic search
        query_embedding = self.embedding_model.encode([query], convert_to_tensor=True).cpu().numpy()
        faiss.normalize_L2(query_embedding)
        _, faiss_indices = self.faiss_index.search(query_embedding, k=top_k*2)
        
        # Keyword search
        bm25_scores = self.bm25.get_scores(query.split())
        bm25_indices = np.argsort(bm25_scores)[-top_k*2:][::-1]
        
        # Combine results
        all_indices = set(faiss_indices[0].tolist() + bm25_indices.tolist())
        
        # Rerank with cross-encoder
        pairs = [(query, self.documents[i]['text']) for i in all_indices]
        rerank_scores = self.cross_encoder.predict(pairs)
        
        final_indices = [i for _, i in sorted(zip(rerank_scores, all_indices), reverse=True)[:top_k]]
        return final_indices
# 3. Answer Generator
class AnswerGenerator:
    def __init__(self, model_name='google/flan-t5-base'):
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.answer_pattern = re.compile(r'\d+%|\$\d+ million|\d{4}')
    
    def generate(self, context, query):
        prompt = f"""Answer truthfully using only this context:
        {context}
        
        Question: {query}
        If the answer isn't in the context, respond 'Not found'.
        Answer:"""
        
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=50,
            num_beams=5,
            early_stopping=True
        )
        
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self.validate_answer(answer)
    
    def validate_answer(self, answer):
        if 'not found' in answer.lower():
            return "Answer not found in documents"
        
        # Extract key numerical facts
        matches = self.answer_pattern.findall(answer)
        if matches:
            return f"{answer} [Validated: {', '.join(matches)}]"
        return answer

# 4. Test Questions
TEST_QUESTIONS = [
    {
        'question': 'What is the revenue growth percentage?',
        'answer': '14%',
        'expected_source': '2023_financial_report.pdf'
    },
    {
        'question': 'Which technology improved operations?',
        'answer': 'AI-driven risk management',
        'expected_source': 'tech_innovation.docx'
    },
    {
        'question': 'What is the market share of the company?',
        'answer': '12.5%',
        'expected_source': 'market_analysis.pdf'
    }
]

# Main Execution
def main():
    # Load data
    documents = load_filtered_chunks("train_t.json")
    print(f"Loaded {len(documents)} chunks from first 10 files")
    
    # Initialize components
    retriever = HybridRetriever()
    retriever.index(documents)
    
    generator = AnswerGenerator()
    
    # Test with QA pairs
    for test in TEST_QUESTIONS:
        print(f"\nQuestion: {test['question']}")
        print(f"Expected Answer: {test['answer']}")
        
        # Retrieve context
        doc_indices = retriever.search(test['question'])
        context = "\n".join([documents[i]['text'] for i in doc_indices])
        
        # Generate answer
        answer = generator.generate(context, test['question'])
        
        # Verify source
        sources = {documents[i]['metadata']['filename'] for i in doc_indices}
        source_match = test['expected_source'] in sources
        
        print(f"Generated Answer: {answer}")
        print(f"Source Match: {'✅' if source_match else '❌'} (Expected: {test['expected_source']})")

if __name__ == "__main__":
    main()