import re


def parse_chunks_file(file_path):
    """Parse chunks_output.txt into a list of chunk dictionaries."""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split by 'ID:' to avoid losing any chunks
    parts = re.split(r"\n(?=ID:\s*)", content)

    parsed_chunks = []
    company_id_pattern = r"^.+?_Q[1-4]\s20\d{2}\.txt$"

    for part in parts:
        id_match = re.search(r"ID:\s*(.+?)(?:\n|$)", part, re.IGNORECASE)
        if not id_match:
            print("❌ Skipping section without ID header.")
            continue

        company_id = id_match.group(1).strip()
        if not re.match(company_id_pattern, company_id):
            print(f"❌ Invalid company ID format: {company_id}")
            continue

        # Extract chunks within this section
        chunk_bodies = re.split(r"Chunk \d+:", part)
        chunk_bodies = [c.strip() for c in chunk_bodies if c.strip()][1:]  # Skip header

        for idx, chunk_text in enumerate(chunk_bodies):
            parsed_chunks.append({
                "company_id": company_id,
                "chunk_id": f"{company_id}_{idx+1}",
                "content": chunk_text,
                "sequence": idx+1
            })
            print(f"✅ Parsed chunk {idx+1} for company: {company_id}")

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
    company_ids = set(chunk["company_id"] for chunk in chunks if chunk["company_id"])
    print("✅ Chunk parsing validated successfully")
    return True


if __name__ == "__main__":
    chunks_file_path = "test_files/chunks_output.txt"
    parsed_chunks = parse_chunks_file(chunks_file_path)
    parsing_valid = validate_chunk_parsing(parsed_chunks)
    if parsing_valid:
        print(f"✅ Parsed {len(parsed_chunks)} chunks")
        unique_companies = set(chunk["company_id"] for chunk in parsed_chunks)
        print(f"Unique companies found: {unique_companies}")
