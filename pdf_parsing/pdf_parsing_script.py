

import numpy as np
import os
import json
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer

# Set up Sentence-Transformers model for local embedding generation
MODEL_NAME = "all-MiniLM-L6-v2"  # Model to use for generating embeddings
model = SentenceTransformer(MODEL_NAME)

# Directory to store embeddings
EMBEDDINGS_DIR = "embeddings"
print(f"Initialized Sentence-Transformer model: {MODEL_NAME}")

# Function to generate embedding locally using Sentence-Transformers model
def get_embedding(text):
    try:
        print(f"Generating embedding for text of length {len(text)}...")
        # Get the embedding for the text
        embedding = model.encode(text)
        
        # Debugging: Check the shape of embeddings
        print(f"Embedding shape: {embedding.shape}")
        
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None  # Return None if embedding generation fails

# Function to chunk the text based on paragraphs
def chunk_text(text, max_chunk_size=512):
    print(f"Chunking text with max chunk size {max_chunk_size}...")
    paragraphs = text.split('\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk + paragraph) > max_chunk_size:
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            current_chunk += " " + paragraph
    
    if current_chunk:
        chunks.append(current_chunk)
    
    print(f"Text chunked into {len(chunks)} chunks.")
    return chunks

# Function to save embeddings and chunked data
def save_embeddings(chunks, embeddings, file_name):
    print(f"Saving embeddings and chunks for file: {file_name}")
    if not os.path.exists(EMBEDDINGS_DIR):
        os.makedirs(EMBEDDINGS_DIR)
        print(f"Created directory: {EMBEDDINGS_DIR}")

    embeddings_file = os.path.join(EMBEDDINGS_DIR, f"{file_name}_embeddings.npy")
    chunks_file = os.path.join(EMBEDDINGS_DIR, f"{file_name}_chunks.json")
    
    print(f"Saving embeddings to: {embeddings_file}")
    np.save(embeddings_file, embeddings.astype("float32"))
    
    print(f"Saving chunks to: {chunks_file}")
    with open(chunks_file, 'w') as f:
        json.dump(chunks, f)
    
    print(f"Embeddings and chunks saved successfully.")
    return embeddings_file, chunks_file

# Function to load saved embeddings and chunks
def load_saved_embeddings(file_name):
    embeddings_file = os.path.join(EMBEDDINGS_DIR, f"{file_name}_embeddings.npy")
    chunks_file = os.path.join(EMBEDDINGS_DIR, f"{file_name}_chunks.json")
    
    print(f"Checking if saved embeddings exist for file: {file_name}")
    if os.path.exists(embeddings_file) and os.path.exists(chunks_file):
        print(f"Found saved embeddings for file: {file_name}")
        embeddings = np.load(embeddings_file)
        with open(chunks_file, 'r') as f:
            chunks = json.load(f)
        return chunks, torch.tensor(embeddings)
    
    print(f"No saved embeddings found for file: {file_name}")
    return None, None

# Function to embed the text file content
def embed_text_file(file_path):
    try:
        print(f"Embedding text from file: {file_path}")
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Break the text into chunks for embedding
        chunks = chunk_text(text)
        
        embeddings = []
        for chunk in chunks:
            if chunk.strip():  # Only process non-empty chunks
                try:
                    embedding = get_embedding(chunk)
                    if embedding is not None:
                        embeddings.append(embedding)
                    else:
                        print(f"Skipping chunk due to embedding failure: {chunk}")
                except Exception as e:
                    print(f"Skipping chunk due to error: {e}")
                    continue
        
        if not embeddings:
            raise ValueError("No valid embeddings were generated. Please check your text file.")
        
        # Convert embeddings to a NumPy array for FAISS indexing
        embeddings = np.vstack(embeddings).astype("float32")  # Ensures proper stacking of embeddings
        
        # Debugging: Check the shape of the embeddings array
        print(f"Embeddings array shape: {embeddings.shape}")
        
        # Build FAISS index
        print("Building FAISS index...")
        index = faiss.IndexFlatL2(embeddings.shape[1])  # Using L2 distance metric
        index.add(embeddings)
        
        print("FAISS index built successfully.")
        return index, chunks
    except Exception as e:
        print(f"Error embedding text file: {e}")
        raise ValueError(f"Error embedding text file: {e}")

# Function to query the Groq API for generating responses based on input query
def query_groq_api(prompt):
    try:
        from groq import Groq
        client = Groq(api_key="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")

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Generate response from Groq LLM
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        
        return response
    except Exception as e:
        print(f"Error querying Groq API: {e}")
        raise ValueError(f"Error querying Groq API: {e}")


# Streamlit UI
def run_app():
    try:
        st.title("RAG System for Financial Report Analysis")
        
        print("Streamlit app initialized. Waiting for file upload...")
        
        # File upload
        uploaded_file = st.file_uploader("Upload your text file", type="txt")
        if uploaded_file is not None:
            # Get the file name
            file_name = uploaded_file.name.split('.')[0]
            print(f"Uploaded file: {file_name}")
            
            # Check if embeddings for this file already exist
            chunks, embeddings = load_saved_embeddings(file_name)
            
            if chunks is None or embeddings is None:
                # Save uploaded file temporarily
                with open("uploaded_file.txt", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                print(f"Saved uploaded file: uploaded_file.txt")
                
                # Embed text file and create FAISS index
                try:
                    index, chunks = embed_text_file("uploaded_file.txt")
                    save_embeddings(chunks, embeddings, file_name)
                    st.success("Text file has been embedded and indexed.")
                    print("Text file successfully embedded and indexed.")
                except Exception as e:
                    st.error(f"Error embedding text: {e}")
            else:
                st.write("Loaded existing embeddings for this file.")
                print("Loaded existing embeddings.")
            
        # User query input
        user_query = st.text_input("Ask a question related to the financial report:")
        
        if user_query:
            print(f"User query: {user_query}")
            
            # Perform the query on FAISS index to find relevant chunks
            try:
                query_embedding = get_embedding(user_query)
                
                # Ensure the query embedding is 2D (shape: 1, embedding_dim)
                query_embedding = query_embedding.reshape(1, -1).astype("float32")
                print(f"Query embedding shape: {query_embedding.shape}")
                
                # Retrieve the most relevant chunk
                print("Searching FAISS index for the most relevant chunk...")
                D, I = index.search(query_embedding, k=1)  # Top 1 result
                
                # Debugging: Print the shapes and content of D and I
                print(f"D shape: {D.shape}, I shape: {I.shape}")
                print(f"D: {D}")
                print(f"I: {I}")
                
                # Check the index I to ensure it's not empty
                if I.size == 0:
                    raise ValueError("No similar chunk found for the query.")

                # Ensure correct handling of I (indices returned from FAISS)
                if len(I.shape) == 2 and I.shape[1] > 0:
                    relevant_chunk = chunks[I[0][0]]  # Corrected handling of index
                else:
                    raise ValueError("Unexpected structure in index search results.")

                # Create the prompt for the Groq API using the relevant chunk and user query
                prompt = f"Based on the following data:\n{relevant_chunk}\n\nAnswer the following question: {user_query}"
                
                # Query Groq API with the generated prompt
                print(f"Generated prompt for Groq API: {prompt[:100]}...")  # Print part of prompt for logging
                response = query_groq_api(prompt)
                
                # Display the response
                st.write("Answer from Groq Model:")
                st.write(response)
                print(f"Response from Groq Model: {response}")
            
            except Exception as e:
                st.error(f"Error with query processing: {e}")
                print(f"Error with query processing: {e}")
    
    except Exception as e:
        st.error(f"Unexpected error in app: {e}")
        print(f"Unexpected error in app: {e}")

if __name__ == "__main__":
    run_app()
