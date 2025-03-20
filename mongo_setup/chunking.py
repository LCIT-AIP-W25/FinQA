import re

def parse_chunks_file(file_path):
    """Parse chunks_output.txt into a list of chunk dictionaries."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Split content into chunks using "Chunk" as a delimiter
    chunks = re.split(r"Chunk \d+:", content)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    
    parsed_chunks = []
    current_company_id = None
    chunk_counter = 0
    
    for i, chunk in enumerate(chunks):
        print(f"\nProcessing chunk {i+1}: {chunk[:100]}...")  # Debug: Print first 100 chars of each chunk
        
        # Look for ID: anywhere in the chunk (not just at the start)
        id_match = re.search(r"ID:\s*(.+?)(?:\n|$)", chunk, re.IGNORECASE)
        if id_match:
            # Update company ID and reset chunk counter for the new company
            current_company_id = id_match.group(1).strip()
            # Split the chunk at the ID: line and take the part after it
            _, chunk_text = re.split(r"ID:\s*.+?(?:\n|$)", chunk, 1, flags=re.IGNORECASE)
            chunk_text = chunk_text.strip()
            chunk_counter = 0  # Reset counter for the new company
            print(f"Detected new company ID: {current_company_id}")
        else:
            # If no ID is found, use the current company ID (if available)
            chunk_text = chunk.strip()
            if not current_company_id:
                print(f"Warning: No company ID found for chunk {i+1}, using 'unknown'")
                current_company_id = "unknown"
        
        if chunk_text:
            chunk_counter += 1
            chunk_id = f"{current_company_id}_{chunk_counter}" if current_company_id else f"unknown_{i}"
            parsed_chunk = {
                "company_id": current_company_id,
                "chunk_id": chunk_id,
                "content": chunk_text,
                "sequence": chunk_counter
            }
            parsed_chunks.append(parsed_chunk)
            print(f"Added chunk: company_id={current_company_id}, chunk_id={chunk_id}, sequence={chunk_counter}")
        else:
            print(f"Skipping empty chunk {i+1}")
    
    return parsed_chunks

def validate_chunk_parsing(chunks):
    """Validate the parsed chunks."""
    if not chunks:
        print("❌ No chunks were parsed")
        return False
    required_keys = ["company_id", "chunk_id", "content", "sequence"]
    for key in required_keys:
        if not all(key in chunk for chunk in chunks):
            print(f"❌ Missing required key '{key}' in some chunks")
            return False
    if not any(chunk["company_id"] for chunk in chunks):
        print("❌ No chunks with company IDs were found")
        return False
    # Check for diverse company IDs
    company_ids = set(chunk["company_id"] for chunk in chunks if chunk["company_id"])
    if len(company_ids) < 2 and any(chunk["company_id"] for chunk in chunks):
        print(f"⚠️ Warning: Only {len(company_ids)} unique company IDs found: {company_ids}")
    print("✅ Chunk parsing validated successfully")
    return True

if __name__ == "__main__":
    # Test parsing
    chunks_file_path = "test_files/chunks_output.txt"  # Adjust path as needed
    parsed_chunks = parse_chunks_file(chunks_file_path)
    parsing_valid = validate_chunk_parsing(parsed_chunks)
    if parsing_valid:
        print(f"✅ Parsed {len(parsed_chunks)} chunks")
        unique_companies = set(chunk["company_id"] for chunk in parsed_chunks if chunk["company_id"])
        print(f"Unique companies found: {unique_companies}")