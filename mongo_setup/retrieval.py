import os
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_groq import ChatGroq  # assuming you're using langchain-groq integration
from embedding import init_embeddings, validate_embedding_model

# Load .env
load_dotenv()

# ------------------- MongoDB Connection ------------------- #
def connect_to_mongo():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_ATLAS_URI not found in .env file")

        client = MongoClient(mongo_uri)
        db = client["Financial_Rag_DB"]
        collection = db["test_files"]
        print("✅ Connected to MongoDB Atlas")
        return collection
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None

def validate_mongo_connection(collection):
    try:
        count = collection.estimated_document_count()
        print(f"✅ MongoDB Collection validated: {count} documents found")
        return True
    except Exception as e:
        print(f"❌ MongoDB validation failed: {e}")
        return False
pyt
# ------------------- Groq LLM Connection ------------------- #
def connect_to_groq():
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")

        llm = ChatGroq(temperature=0.2, model="mixtral-8x7b-32768", api_key=groq_api_key)
        print("✅ Connected to Groq LLM")
        return llm
    except Exception as e:
        print(f"❌ Groq LLM connection failed: {e}")
        return None

# ------------------- Vector Store ------------------- #
def init_vector_store(collection, embeddings):
    try:
        vector_store = MongoDBAtlasVectorSearch(
            collection=collection,
            embedding=embeddings,
            index_name="st_vector_index",
            embedding_key="embedding",
            text_key="content"
        )
        print("✅ Vector store initialized")
        return vector_store
    except Exception as e:
        print(f"❌ Vector store initialization failed: {e}")
        return None

# ------------------- Document Retrieval ------------------- #
def retrieve_documents(vector_store, question, k=2):
    try:
        retrieved_docs = vector_store.similarity_search(question, k=k)
        print(f"✅ Retrieved {len(retrieved_docs)} documents")
        return retrieved_docs
    except Exception as e:
        print(f"❌ Document retrieval failed: {e}")
        return []

def validate_retrieval(docs, expected_count=2):
    if len(docs) >= expected_count:
        print(f"✅ Retrieval validation successful: Retrieved {len(docs)} documents")
        for i, doc in enumerate(docs):
            print(f"\nDocument {i+1}:")
            print(f"Content: {doc.page_content[:200]}...")
            print(f"Metadata: {doc.metadata}")
        return True
    else:
        print(f"❌ Retrieval validation failed: Expected at least {expected_count} documents, got {len(docs)}")
        return False

# ------------------- Main Pipeline ------------------- #
if __name__ == "__main__":
    # 1. Connect to MongoDB
    collection = connect_to_mongo()
    if not validate_mongo_connection(collection):
        exit()

    # 2. Connect to Groq
    llm = connect_to_groq()
    if not llm:
        exit()

    # 3. Init embeddings
    embeddings = init_embeddings()
    if not validate_embedding_model(embeddings):
        exit()

    # 4. Init Vector Store
    vector_store = init_vector_store(collection, embeddings)
    if not vector_store:
        exit()

    # 5. Retrieve documents and pass to Groq LLM
    sample_question = "What are AMD's forward-looking statements about?"
    retrieved_docs = retrieve_documents(vector_store, sample_question)

    if validate_retrieval(retrieved_docs):
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        prompt = f"Based on the following information, answer the question:\n\n{context}\n\nQuestion: {sample_question}"

        response = llm.invoke(prompt)
        print("\n🎯 LLM Response:")
        print(response.content)
