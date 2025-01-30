import os
import numpy as np
import faiss
from langchain_huggingface import HuggingFaceEmbeddings 
import ollama
from string import Template

# Load embeddings model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_documents(directory):
    """Load text documents from a given directory."""
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

# Define the directory containing documents
document_dir = r'C:\Users\palas\Desktop\AIP\documents'
documents = load_documents(document_dir)

# Generate embeddings for all documents
document_embeddings = embeddings.embed_documents(documents)

# Convert embeddings to numpy array
document_embeddings = np.array(document_embeddings).astype('float32')

# Create FAISS index
index = faiss.IndexFlatL2(document_embeddings.shape[1])  # L2 distance metric
index.add(document_embeddings)  # Add document embeddings to the index

class SimpleRetriever:
    """Simple FAISS-based retriever class."""
    def __init__(self, index, embeddings, documents):
        self.index = index
        self.embeddings = embeddings
        self.documents = documents
    
    def retrieve(self, query, k=3):
        query_embedding = self.embeddings.embed_query(query)
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        return [self.documents[i] for i in indices[0] if i < len(self.documents)]

retriever = SimpleRetriever(index, embeddings, documents)

# Craft the prompt template using string.Template for better readability
prompt_template = Template("""
Use ONLY the context below.
If unsure, say "I don't know".
Keep answers under 4 sentences.

Context: $context
Question: $question
Answer:
""")

def answer_query(question, retriever):
    # Retrieve relevant context
    context = retriever.retrieve(question)
    combined_context = "\n".join(context)

    # Generate response using Ollama
    response = ollama.generate(
        model="deepseek-r1:1.5b",
        prompt=prompt_template.substitute(context=combined_context, question=question)
    )

    return response['response'].strip()

if __name__ == "__main__":
    user_question = input("Enter your question: ")
    answer = answer_query(user_question, retriever)
    print("Answer:", answer)
