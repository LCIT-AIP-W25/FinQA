import pymongo
import json
import logging

# Configure logging to track issues
logging.basicConfig(
    filename="upload_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# MongoDB Connection URI
MONGO_URI = "mongodb+srv://usr:pwd@finqa.ywfoq.mongodb.net/?retryWrites=true&w=majority&appName=FinQA"

# Connect to MongoDB Atlas
try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["FinQA"]
    print("Connection to MongoDB successful!")
except pymongo.errors.ConnectionError as e:
    print("Failed to connect to MongoDB:", e)
    exit()

# Define collections
financial_data_collection = db["financial_data"]
paragraphs_collection = db["paragraphs"]
qa_dataset_collection = db["qa_dataset"]

# Load cleaned JSON data
try:
    with open("cleaned_financial_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    print(f"Loaded {len(data)} entries from the cleaned data.")
except FileNotFoundError:
    print("File 'cleaned_financial_data.json' not found.")
    exit()
except json.JSONDecodeError as e:
    print("Error decoding JSON file:", e)
    exit()

# Prepare records for insertion
financial_data_records = []
paragraph_records = []
qa_records = []

for entry in data:
    table_uid = entry.get("table_uid", "unknown")

    # Validate and append financial data
    for record in entry.get("financial_data", []):
        if record and "category" in record:
            financial_data_records.append({
                "table_uid": table_uid,
                "category": record.get("category"),
                "values": {k: v for k, v in record.items() if k.isdigit()}
            })
        else:
            logging.error(f"Invalid financial record skipped: {record}")

    # Validate and append paragraphs
    for paragraph in entry.get("paragraphs", []):
        if paragraph and "text" in paragraph:
            paragraph_records.append({
                "paragraph_uid": paragraph.get("uid", "unknown"),
                "table_uid": table_uid,
                "order": paragraph.get("order", 0),
                "text": paragraph.get("text", "").strip()
            })
        else:
            logging.error(f"Invalid paragraph skipped: {paragraph}")

    # Validate and append Q&A dataset
    for qa in entry.get("questions", []):
        if qa and "question" in qa:
            qa_records.append({
                "qa_uid": qa.get("uid", "unknown"),
                "table_uid": table_uid,
                "question": qa["question"].strip(),
                "answer": qa.get("answer", []),
                "answer_type": qa.get("answer_type", ""),
                "rel_paragraphs": qa.get("rel_paragraphs", [])
            })
        else:
            logging.error(f"Invalid QA record skipped: {qa}")

# Function to upload data in batches
def upload_to_collection(collection, records, collection_name):
    if not records:
        print(f"No valid records for {collection_name}.")
        return

    batch_size = 100  # Upload in smaller batches
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        try:
            result = collection.insert_many(batch, ordered=False)
            print(f"Uploaded {len(result.inserted_ids)} records to '{collection_name}' collection (Batch {i // batch_size + 1}).")
        except pymongo.errors.BulkWriteError as e:
            logging.error(f"Error inserting batch {i // batch_size + 1} into '{collection_name}': {e.details}")
            print(f"Error inserting some records into '{collection_name}'. Check upload_errors.log for details.")

# Upload to MongoDB
print("Uploading financial data...")
upload_to_collection(financial_data_collection, financial_data_records, "financial_data")

print("Uploading paragraphs...")
upload_to_collection(paragraphs_collection, paragraph_records, "paragraphs")

print("Uploading Q&A dataset...")
upload_to_collection(qa_dataset_collection, qa_records, "qa_dataset")

# Close the connection
client.close()
print("Upload complete and connection to MongoDB closed.")
