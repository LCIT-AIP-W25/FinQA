import re
import json
import os

def sanitize_filename(name):
    """Sanitizes a filename by replacing invalid characters with underscores."""
    return re.sub(r'[\\/:*?"<>|]', '_', name)


def convert_to_proper_type(value, is_first_column=False):
    """Converts a value to its appropriate type: int, float, or leaves it as a string if it contains text."""
    if not isinstance(value, str) or not value.strip():
        return value

    value = value.strip()

    if is_first_column:
        if re.fullmatch(r'\d+', value):
            return int(value)
        return value

    # Handle negative numbers formatted as $(X)
    if re.fullmatch(r'\$\(\d{1,3}(,\d{3})*(\.\d+)?\)', value):  # Example: $(7,413) or $(6.23)
        return -float(value.strip('$()').replace(',', '')) if '.' in value else -int(value.strip('$()').replace(',', ''))

    # Handle negative numbers formatted as (X) without $
    if re.fullmatch(r'\(\d{1,3}(,\d{3})*(\.\d+)?\)', value):  # Example: (7,413) or (6.23)
        return -float(value.strip('()').replace(',', '')) if '.' in value else -int(value.strip('()').replace(',', ''))

    # Handle standard numeric values with or without $
    if re.fullmatch(r'\$?\d{1,3}(,\d{3})*(\.\d+)?', value):  # Example: 1000, $1000, 1,000.50
        return float(value.replace(',', '').replace('$', '')) if '.' in value else int(value.replace(',', '').replace('$', ''))

    return value


def sanitize_header(value):
    """Removes HTML tags and numeric annotations from headers."""
    if not isinstance(value, str):
        return value

    value = re.sub(r'<[^>]*>', '', value)  # Remove HTML tags
    value = re.sub(r'\(\d+\)', '', value)  # Remove (1), (2) annotations
    return value.strip()


def clean_table_ori(table_ori):
    """Cleans the given table by sanitizing headers and properly converting values."""
    if not table_ori or not isinstance(table_ori, list):
        return table_ori

    # Step 1: Ensure the first row (header) has no blanks
    if len(table_ori) > 0 and table_ori[0]:
        table_ori[0] = [sanitize_header(cell) if cell else "Placeholder" for cell in table_ori[0]]

    # Step 2: Clean each row and convert types
    processed_table = []
    for i, row in enumerate(table_ori):
        processed_row = [
            convert_to_proper_type(cell, is_first_column=(j == 0)) for j, cell in enumerate(row)
        ]
        processed_table.append(processed_row)

    return processed_table


def process_and_clean_data_for_companies(file_path, output_folder):
    """Processes a JSON file, cleans the data, and saves the cleaned data."""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return

    companies = set(item.get('id', '').split('_')[1] for item in data if 'id' in item)
    os.makedirs(output_folder, exist_ok=True)

    for company in companies:
        print(f"Processing data for company: {company}")
        sanitized_company = sanitize_filename(company)
        filtered_data = []

        for item in data:
            if company in item.get('filename', ''):
                cleaned_table_ori = clean_table_ori(item.get("table_ori", []))
                filtered_data.append({
                    "id": item.get("id", ""),
                    "filename": item.get("filename", ""),
                    "table_ori": cleaned_table_ori
                })

        output_file = os.path.join(output_folder, f"{sanitized_company}_cleaned_data.json")
        try:
            with open(output_file, 'w') as f:
                json.dump(filtered_data, f, indent=4)
            print(f"Saved cleaned data for {company} to {output_file}")
        except IOError as e:
            print(f"Error: Unable to write to file {output_file}. {e}")


# Example usage
file_path = r'C:\Users\user\OneDrive - Loyalist College\AIandDS\Term 4\FinQ&A\train_t.json'
output_folder = 'cleaned_data'
process_and_clean_data_for_companies(file_path, output_folder)