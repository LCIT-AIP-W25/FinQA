import re
import json
import os
import locale
import unicodedata
import hashlib

# Set locale to US (to recognize comma as thousands separator)
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def remove_html_tags(value):
    """Removes HTML tags (e.g., <sup>, <b>, <i>) from any string."""
    if isinstance(value, str):
        return re.sub(r'<[^>]*>', '', value).strip()
    return value  # Return as-is if not a string

def format_numeric_value_locale(value):
    """
    Converts numeric values into the appropriate type using `locale.atof()`.
    Handles:
    - Negative numbers formatted as $(X) or (X)
    - Negative numbers with dollar signs: -$X, $-X
    - Standard numbers with commas and dollar signs
    - Percentages (e.g., "34%") -> 0.34
    - Unicode dashes (e.g., $—, —, –, etc.) -> Converts to 0
    """
    if not isinstance(value, str):
        return value

    value = remove_html_tags(value).strip()
    value = unicodedata.normalize("NFKD", value)  # Normalize Unicode

    # Convert Unicode dashes to 0
    if value in [
                "\u2007", "$\u2007", "-\u2007",
                "\u2008", "$\u2008", "-\u2008",
                "\u2009", "$\u2009", "-\u2009",
                "\u2010", "$\u2010", "-\u2010",
                "\u2011", "$\u2011", "-\u2011",
                "\u2012", "$\u2012", "-\u2012",
                "\u2013", "$\u2013", "-\u2013",
                "\u2014", "$\u2014", "-\u2014",
                "\u2015", "$\u2015", "-\u2015",
                "\u2016", "$\u2016", "-\u2016",
                "\u2017", "$\u2017", "-\u2017",
                "\u2018", "$\u2018", "-\u2018",
                "\u2019", "$\u2019", "-\u2019",
                "\u2020", "$\u2020", "-\u2020"
                ]:
        return 0

    # Handle negative numbers formatted as $(X)
    if value.startswith("($") and value.endswith(")"):
        value = "-" + value.strip("($)").replace(",", "")
    elif value.startswith("(") and value.endswith(")"):
        value = "-" + value.strip("()").replace(",", "")
    elif value.startswith("$(") and value.endswith(")"):
        value = "-" + value.strip("$()").replace(",", "")

    # Handle negative numbers formatted as -$X or $-X
    elif value.startswith("-$") or value.startswith("$-"):
        value = "-" + value.strip("-$").replace(",", "")

    # Handle negative numbers formatted as "- X" or "-X"
    elif value.startswith("- "):
        value = "-" + value.strip("- ").replace(",", "")
    elif value.startswith("-"):
        value = "-" + value.strip("-").replace(",", "")

    # Handle percentage values
    if value.endswith("%"):
        try:
            return locale.atof(value.strip("%")) / 100
        except ValueError:
            return value

    # Remove dollar sign and parse number
    clean_value = value.replace("$", "")

    try:
        num = locale.atof(clean_value)
        return int(num) if num.is_integer() else num
    except ValueError:
        return value

def generate_column_names(header_row):
    """Generates unique column names for missing or blank headers."""
    new_headers = []
    seen_headers = set()

    for i, header in enumerate(header_row):
        clean_header = remove_html_tags(header)
        new_name = f"Column_{i+1}" if not clean_header else clean_header

        # Ensure uniqueness
        count = 1
        while new_name in seen_headers:
            new_name = f"{clean_header}_{count}"
            count += 1

        seen_headers.add(new_name)
        new_headers.append(new_name)

    return new_headers

def replace_missing_values(row):
    """Replaces empty cells in any row with 'Missing_Value'."""
    return ["Missing_Value" if (cell == "" or cell is None) else cell for cell in row]

def remove_empty_rows(table_ori):
    """Removes completely empty rows from `table_ori`."""
    return [row for row in table_ori if not all(cell in ["", None, "Missing_Value"] for cell in row)]

def hash_table_ori(table_ori):
    """Generates a unique hash for the table_ori to detect duplicates."""
    table_str = json.dumps(table_ori, sort_keys=True)  # Convert to string (sorted for consistency)
    return hashlib.md5(table_str.encode()).hexdigest()  # Generate MD5 hash

def remove_duplicate_entries(data):
    """Removes duplicate `table_ori` entries based on content."""
    unique_tables = set()
    cleaned_data = []

    for entry in data:
        table_hash = hash_table_ori(entry["table_ori"])

        if table_hash not in unique_tables:
            unique_tables.add(table_hash)
            cleaned_data.append(entry)

    return cleaned_data

def clean_table_ori(table_ori):
    """
    Cleans the `table_ori` structure dynamically:
    - Fixes numeric formatting (currency, percentages, negative numbers).
    - Removes HTML tags from headers and data values.
    - Generates placeholders for missing or blank headers.
    - Replaces missing values in any row with "Missing_Value".
    - Removes completely empty rows.
    """
    if not table_ori or not isinstance(table_ori, list):
        return table_ori

    # Step 1: Clean first row (headers)
    if len(table_ori) > 0:
        table_ori[0] = generate_column_names(table_ori[0])

    # Step 2: Convert values and replace missing ones
    cleaned_table = [table_ori[0]]
    for row in table_ori[1:]:
        row = replace_missing_values(row)
        cleaned_row = [format_numeric_value_locale(cell) for cell in row]
        cleaned_table.append(cleaned_row)

    # Step 3: Remove empty rows
    return remove_empty_rows(cleaned_table)

def extract_company_year(filename):
    """Extracts company name and year from the filename."""
    match = re.search(r'([A-Z]+)[/_](\d{4})', filename)
    return match.groups() if match else (None, None)

def sanitize_filename(name):
    """Sanitizes a string for valid filenames."""
    return re.sub(r'[\/:*?"<>|]', '_', name)

def process_and_clean_data_for_companies(file_path, output_folder):
    """Processes, cleans, removes duplicates, and saves cleaned data."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Unable to read JSON file {file_path}.")
        return

    os.makedirs(output_folder, exist_ok=True)

    for item in data:
        filename = item.get("filename", "")
        company, year = extract_company_year(filename)

        if company and year:
            sanitized_company = sanitize_filename(company)
            output_file = os.path.join(output_folder, f"{sanitized_company}_{year}_cleaned_data.json")

            cleaned_table_ori = clean_table_ori(item.get("table_ori", []))
            cleaned_data = {
                "id": item.get("id", ""),
                "filename": item.get("filename", ""),
                "table_ori": cleaned_table_ori
            }

            # Check if file already exists to append data
            try:
                if os.path.exists(output_file):
                    with open(output_file, 'r+', encoding='utf-8') as f:
                        existing_data = json.load(f)
                        existing_data.append(cleaned_data)
                        f.seek(0)
                        json.dump(remove_duplicate_entries(existing_data), f, indent=4)  # Remove duplicates
                else:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump([cleaned_data], f, indent=4)
                print(f"Saved cleaned data for {company} ({year}) to {output_file}")
            except IOError as e:
                print(f"Error: Unable to write to file {output_file}. {e}")

# Example Usage
file_path = r"C:\Users\user\OneDrive - Loyalist College\AIandDS\Term 4\FinQ&A\train_t.json"
output_folder = r"cleaned_data_new"

# Run script
process_and_clean_data_for_companies(file_path, output_folder)