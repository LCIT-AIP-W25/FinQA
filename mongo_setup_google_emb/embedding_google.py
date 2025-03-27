import time
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ingestion import connect_to_mongo, validate_mongo_connection

# Load environment variables
load_dotenv()

# Load multiple Google API keys
GOOGLE_API_KEYS = [
    os.getenv("GOOGLE_API_KEY1"),
    os.getenv("GOOGLE_API_KEY2"),
    os.getenv("GOOGLE_API_KEY3"),
]

def validate_embedding_model(api_key):
    """Validate a single Google API key."""
    try:
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        sample_text = "This is a test document."
        embedding = embedding_model.embed_query(sample_text)
        print(f"✅ API Key validated: {api_key[:20]}... | Dim: {len(embedding)}")
        return True
    except Exception as e:
        print(f"❌ Embedding model failed for key {api_key[:20]}...: {e}")
        return False

def generate_and_store_embeddings(collection):
    """Embed documents with rotated API keys and 1-second delays."""
    total_docs = collection.count_documents({})
    docs_to_embed = list(collection.find({"embedding": {"$exists": False}}, {"content": 1, "_id": 1}))
    docs_with_embeddings = collection.count_documents({"embedding": {"$exists": True}})

    if not docs_to_embed:
        print(f"✅ All {total_docs} documents already have embeddings.")
        return True

    print(f"📦 Total documents: {total_docs}")
    print(f"🧠 Already embedded: {docs_with_embeddings}")
    print(f"🆕 To embed: {len(docs_to_embed)}\n")

    total_keys = len(GOOGLE_API_KEYS)

    for idx, doc in enumerate(docs_to_embed, 1):
        text = doc.get("content", "").strip()
        _id = doc["_id"]
        key_index = idx % total_keys
        current_key = GOOGLE_API_KEYS[key_index]

        # Initialize embedding model with current key
        try:
            embedding_model = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=current_key
            )
        except Exception as e:
            print(f"❌ Failed to init model with key {key_index+1}: {e}")
            continue

        # Retry embedding
        for attempt in range(3):
            try:
                embedding = embedding_model.embed_query(text)
                break
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed for _id {_id} with key {key_index+1}: {e}")
                time.sleep(2)
        else:
            print(f"❌ Skipped _id {_id} after 3 failed attempts.")
            continue

        # Save embedding
        collection.update_one({"_id": _id}, {"$set": {"embedding": embedding}})
        print(f"✅ [{idx}/{len(docs_to_embed)}] Embedded _id: {_id} using key #{key_index+1}")

        time.sleep(1)

        if idx % 50 == 0:
            print(f"🔁 Progress: {idx} embedded out of {len(docs_to_embed)}")

    print(f"\n🎉 All documents processed.")
    return True

def validate_embeddings(collection):
    """Check that all documents have been embedded."""
    total_docs = collection.count_documents({})
    with_embeddings = collection.count_documents({"embedding": {"$exists": True}})
    if total_docs == with_embeddings:
        print(f"✅ All {total_docs} documents have embeddings.")
        return True
    else:
        print(f"❌ Only {with_embeddings}/{total_docs} have embeddings.")
        return False

# Entry Point
if __name__ == "__main__":
    collection = connect_to_mongo()
    if validate_mongo_connection(collection):
        print("🔍 Validating all API keys...")
        for key in GOOGLE_API_KEYS:
            validate_embedding_model(key)
        if generate_and_store_embeddings(collection):
            validate_embeddings(collection)
