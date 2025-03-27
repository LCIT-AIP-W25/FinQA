# from pymongo import MongoClient
# import os
# from dotenv import load_dotenv

# load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")

# client = MongoClient(MONGO_URI)
# db = client["Financial_Rag_DB"]
# collection = db["test_files"]

# # Search for Google documents
# query = {
#     "company_id": {"$regex": "Google", "$options": "i"},
#     "content": {"$regex": "stock repurchase|share buyback", "$options": "i"}
# }
# matching_docs = collection.find(query)

# print("Documents related to Google's stock repurchase:")
# for i, doc in enumerate(matching_docs):
#     print(f"Document {i+1}:")
#     print(f"Company ID: {doc['company_id']}")
#     print(f"Chunk ID: {doc['chunk_id']}")
#     print(f"Content: {doc['content'][:500]}...")
#     print()

# client.close()

# import pandas as pd

# df = pd.read_csv("combined_rag_evaluation.csv")
# print(df.columns)


from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://Shekhar_25:Shekhar%402025@cluster0.kjjhc.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection string
collection = client["Financial_Rag_DB"]["test_files"]  # Adjust database and collection names

# Fetch distinct company_id values
distinct_company_ids = collection.distinct("company_id")

# Print the results
print("Distinct company_id values:", distinct_company_ids)

# Optional: If you only want company names (e.g., "Google" from "Google_04_2023_txt")
import re
company_names = set()
for company_id in distinct_company_ids:
    match = re.match(r"^(.*?)_", company_id)  # Extract text before the first underscore
    if match:
        company_names.add(match.group(1))

# Convert to a sorted list for UI display
company_names = sorted(list(company_names))
print("Distinct company names:", company_names)