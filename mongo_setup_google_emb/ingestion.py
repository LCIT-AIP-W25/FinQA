import os
import re
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

def clean_text(text):
    """
    Clean the input text by removing non-printable characters.
    You can customize the regex to better suit your data.
    """
    # Remove any character that is not printable (ASCII 32-126)x
    cleaned = re.sub(r'[^\x20-\x7E]+', ' ', text)
    return cleaned.strip()

def connect_to_mongo():
    """Connect to MongoDB and return the chunks_data collection."""
    try:
        client = MongoClient(MONGO_URI)
        db = client["Financial_Rag_DB"]
        if "chunks_data" in db.list_collection_names():
            collection = db["chunks_data"]
            print("✅ Using existing collection Financial_Rag_DB.chunks_data")
        else:
            collection = db["chunks_data"]
            print("✅ Created new collection Financial_Rag_DB.chunks_data")
        return collection
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        raise

def validate_mongo_connection(collection):
    """Validate the MongoDB connection."""
    try:
        collection.find_one()
        print("✅ MongoDB connection validated")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection validation failed: {e}")
        return False

def store_chunks_in_mongodb(collection, chunks):
    """Store parsed chunks in MongoDB, skipping duplicates.
    This version cleans the text in each chunk before insertion."""
    inserted_count = 0
    skipped_count = 0
    for chunk in chunks:
        # Clean the chunk text to remove artifacts
        chunk['text'] = clean_text(chunk.get('text', ''))
        if collection.find_one({"chunk_id": chunk["chunk_id"]}) is None:
            collection.insert_one(chunk)
            inserted_count += 1
            print(f"Inserted chunk: {chunk['chunk_id']} (company: {chunk['company_id']})")
        else:
            skipped_count += 1
            print(f"Skipped duplicate chunk: {chunk['chunk_id']} (company: {chunk['company_id']})")
    print(f"✅ Inserted {inserted_count} new chunks, skipped {skipped_count} existing chunks")
    return inserted_count > 0 or skipped_count > 0

def validate_mongodb_storage(collection, expected_count):
    """Validate that the expected number of documents are stored."""
    actual_count = collection.count_documents({})
    if actual_count >= expected_count:
        print(f"✅ MongoDB storage validated: {actual_count} documents found")
        # Verify unique company IDs in MongoDB
        unique_companies = collection.distinct("company_id")
        print(f"Unique companies in MongoDB: {unique_companies}")
        return True
    else:
        print(f"❌ MongoDB storage validation failed: Expected at least {expected_count} documents, found {actual_count}")
        return False

if __name__ == "__main__":
    # Example usage for testing
    collection = connect_to_mongo()
    connection_valid = validate_mongo_connection(collection)
    if connection_valid:
        # Normally, chunks would come from chunking.py
        from chunking import parse_chunks_file
        chunks_file_path = "test_files/chunks_output.txt"
        parsed_chunks = parse_chunks_file(chunks_file_path)
        storage_success = store_chunks_in_mongodb(collection, parsed_chunks)
        if storage_success:
            validate_mongodb_storage(collection, len(parsed_chunks))
