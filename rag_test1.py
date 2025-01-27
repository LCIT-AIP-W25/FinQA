import streamlit as st
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
import openai

# Function to clean text
def clean_text(text):
    return " ".join(text.split())

# Updated function for the new OpenAI API (v1.60.1)
def summarize_context(context, query):
    prompt = f"Answer the following question based on the given context:\n\nContext: {context}\n\nQuestion: {query}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Ensure the correct model is used
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()



def extract_metric(text, metric):
    # Look for the full phrase and a number nearby
    pattern = rf"{metric}.*?(\d[\d,\.]*)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return "Metric not found"


# Function to load JSON data
@st.cache_data
def load_json(uploaded_file):
    data = json.load(uploaded_file)
    return data

# Generate embeddings using SentenceTransformers
@st.cache_resource
def generate_embeddings(corpus, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(corpus)
    return model, embeddings

# Build FAISS index for embeddings
@st.cache_resource
def build_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Search function
def search(query, model, index, corpus, top_k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=top_k)
    results = [(corpus[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
    return results

# Streamlit UI
st.title("RAG System for Financial Reports")
st.write("Upload a structured JSON file and query the RAG system for contextual answers.")

# Upload JSON file
uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
if uploaded_file:
    structured_data = load_json(uploaded_file)
    corpus = []
    for section, content in structured_data.items():
        corpus.extend(content)

    # Clean text in corpus
    corpus = [clean_text(doc) for doc in corpus]

    # Generate embeddings and build FAISS index
    st.write("Generating embeddings and building FAISS index...")
    model, embeddings = generate_embeddings(corpus)
    index = build_faiss_index(embeddings)
    st.success(f"FAISS index built with {index.ntotal} documents.")

    # Query the RAG system
    st.write("Enter a query below to test the system.")
    query = st.text_input("Query:")
    if query:
        st.write("Results:")
        results = search(query, model, index, corpus, top_k=3)

        for i, (doc, score) in enumerate(results):
            if "net income" in query.lower():  # Example numerical query
                metric_value = extract_metric(doc, "net income")
                st.markdown(f"**Result {i + 1}: Adjusted Net Income:** {metric_value}\n*Relevance Score:* {score:.4f}")
            else:
                summarized_answer = summarize_context(doc, query)
                st.markdown(f"**Result {i + 1}:**\n{summarized_answer}\n*Relevance Score:* {score:.4f}")
