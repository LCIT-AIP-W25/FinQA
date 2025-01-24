import json
import re

def clean_table(table_data):
    """Convert raw table list into structured key-value pairs, handling edge cases."""
    cleaned_table = []

    if not table_data or "table" not in table_data:
        return cleaned_table  # Return empty if no table exists

    raw_table = table_data["table"]

    # Ensure table has at least two rows (headers + data)
    if len(raw_table) < 2:
        return cleaned_table

    # Extract headers (years, categories), removing unwanted symbols
    headers = [re.sub(r'\D', '', col) for col in raw_table[0][1:] if col.strip()]  # Extract numeric years

    for row in raw_table[1:]:  # Process each row
        category = row[0].strip()
        if not category:  # Ignore empty category names
            continue

        cleaned_row = {"category": category}

        # Process values, ensuring the row length matches the header length
        for i in range(min(len(headers), len(row) - 1)):  # Ensure index alignment
            value = row[i + 1]  # Offset by 1 since the first column is "category"
            clean_value = re.sub(r'[^\d.-]', '', value)  # Remove $, %, commas
            try:
                # Convert to float or None if missing
                cleaned_row[headers[i]] = float(clean_value) if clean_value else None
            except ValueError:
                cleaned_row[headers[i]] = None  # Handle non-numeric values

        cleaned_table.append(cleaned_row)

    return cleaned_table

def clean_json(input_file, output_file):
    """Reads raw JSON, cleans it, and saves structured data."""
    with open(input_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    cleaned_data = []

    for entry in raw_data:
        table_data = clean_table(entry.get("table", {}))  # Clean table
        paragraphs = entry.get("paragraphs", [])
        questions = entry.get("questions", [])

        cleaned_data.append({
            "table_uid": entry["table"].get("uid", "unknown"),
            "financial_data": table_data,
            "paragraphs": paragraphs,
            "questions": questions
        })

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(cleaned_data, file, indent=4)

    print(f"Cleaned data saved to {output_file}")


# Run the cleaning script
clean_json(r"C:\Users\user\OneDrive - Loyalist College\AIandDS\Term 4\FinQ&A\train1.json", "cleaned_financial_data.json")
