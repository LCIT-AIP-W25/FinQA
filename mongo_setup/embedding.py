from langchain_community.embeddings import SentenceTransformerEmbeddings
from ingestion import connect_to_mongo, validate_mongo_connection

def init_embeddings():
    """Initialize the Sentence Transformer embeddings model."""
    embeddings = SentenceTransformerEmbeddings(model_name="sentence-transformers/multi-qa-mpnet-base-cos-v1")
    return embeddings

def validate_embedding_model(embeddings):
    """Validate the embedding model dimensionality."""
    try:
        sample_text = "This is a test document."
        embedding = embeddings.embed_query(sample_text)
        if len(embedding) == 768:
            print(f"✅ Sentence Transformer initialized: Dimensionality = {len(embedding)}")
            return True
        else:
            print(f"❌ Sentence Transformer dimensionality incorrect: Expected 768, got {len(embedding)}")
            return False
    except Exception as e:
        print(f"❌ Sentence Transformer initialization failed: {e}")
        return False

def generate_and_store_embeddings(collection, embeddings):
    """Generate and store embeddings for documents without them."""
    documents = list(collection.find({"embedding": {"$exists": False}}, {"content": 1, "_id": 1}))
    if not documents:
        print("✅ All documents already have embeddings")
        return True
    texts = [doc["content"] for doc in documents]
    ids = [doc["_id"] for doc in documents]
    try:
        embedding_vectors = embeddings.embed_documents(texts)
        for _id, embedding in zip(ids, embedding_vectors):
            collection.update_one(
                {"_id": _id},
                {"$set": {"embedding": embedding}}
            )
        print(f"✅ Generated and stored embeddings for {len(documents)} documents")
        return True
    except Exception as e:
        print(f"❌ Error generating embeddings: {e}")
        return False

def validate_embeddings(collection):
    """Validate that all documents have embeddings."""
    total_docs = collection.count_documents({})
    docs_with_embedding = collection.count_documents({"embedding": {"$exists": True}})
    if docs_with_embedding == total_docs:
        print(f"✅ Embeddings validation successful: All {total_docs} documents have embeddings")
        return True
    else:
        print(f"❌ Embeddings validation failed: {docs_with_embedding}/{total_docs} documents have embeddings")
        return False

if __name__ == "__main__":
    # Test embedding
    collection = connect_to_mongo()
    if validate_mongo_connection(collection):
        embeddings = init_embeddings()
        if validate_embedding_model(embeddings):
            embedding_success = generate_and_store_embeddings(collection, embeddings)
            if embedding_success:
                validate_embeddings(collection)