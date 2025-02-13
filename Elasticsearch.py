import streamlit as st
import pandas as pd
import fitz
import docx
import openpyxl
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch("https://localhost:9200", basic_auth=("elastic", "password"), verify_certs=False)

from elasticsearch import Elasticsearch
import os
import glob

# Define the index name
INDEX_NAME = "documents"

# Delete all documents at the start of every session**
def delete_all_documents():
    print("Deleting all documents from the index...")
    es.delete_by_query(index=INDEX_NAME, body={"query": {"match_all": {}}})
    print("All documents deleted!")

# Index new documents**
def index_documents(folder_path):
    delete_all_documents()  # Delete before indexing

    file_paths = glob.glob(os.path.join(folder_path, "*"))  # Get all files in the folder
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            es.index(index=INDEX_NAME, id=i, document={"content": content, "filename": os.path.basename(file_path)})
            print(f"Indexed: {file_path}")

# Search and highlight context around term**
def search_documents(query):
    response = es.search(index=INDEX_NAME, body={
        "query": {
            "match": {"content": query}
        },
        "highlight": {
            "fields": {
                "content": {
                    "pre_tags": ["\033[1;33m"],  # Yellow color highlight in terminal
                    "post_tags": ["\033[0m"]
                }
            }
        }
    })

    results = response["hits"]["hits"]
    print(f"\nFound {len(results)} document(s) containing '{query}':\n")
    for doc in results:
        filename = doc["_source"]["filename"]
        highlight = doc.get("highlight", {}).get("content", ["No highlight available"])[0]
        print(f"File: {filename}")
        print(f"Excerpt: {highlight}\n")

if __name__ == "__main__":
    folder_path = "your/documents/folder/path"  # Update this with your document folder path
    index_documents(folder_path)  # Delete old docs & index new ones
    search_term = input("\nEnter search query: ")
    search_documents(search_term)  # Perform search with highlight

