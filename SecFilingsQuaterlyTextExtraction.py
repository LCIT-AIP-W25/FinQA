import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from sec_edgar_downloader import Downloader

# Your email (required by SEC)
EMAIL_ADDRESS = "your-email@example.com"

# Initialize SEC Downloader
dl = Downloader("sec-edgar-filings", EMAIL_ADDRESS)

# Define list of companies and their CIKs
companies = {
    "Google": 1652044,
    "Amazon": 1018724,
    "Meta": 1326801,
    "Tesla": 1318605,
    "JP Morgan": 19617,
    "Mastercard": 1141391,
    "Netflix": 1065280,
    "Coca-Cola": 21344,
    "McDonald": 63908,
    "Pepsico": 77476,
    "Shell": 1306965,
    "AMD": 2488,
    "HSBC": 1089113,
    "AT&T": 732717,
    "Verizon": 732712,
    "S&P Global": 64040
}

# Get the current year
current_year = pd.Timestamp.today().year

# Function to determine the quarter in "Qx YYYY" format
def get_quarter(reporting_date, form_type):
    month = reporting_date.month
    year = reporting_date.year

    if form_type == "10-K":  # Q4 data comes from the 10-K report
        return f"Q4 {year}"
    elif 1 <= month <= 3:
        return f"Q1 {year}"
    elif 4 <= month <= 6:
        return f"Q2 {year}"
    elif 7 <= month <= 9:
        return f"Q3 {year}"
    else:
        return "Unknown"

# Function to clean extracted text
def clean_text(text):
    """Remove excessive spaces and newlines."""
    text = re.sub(r'\n+', '\n', text)  # Remove extra newlines
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    return text.strip()

# Function to extract text while **removing only `<table>` content**
def extract_text_without_tables(content):
    """Extracts SEC filing text while **removing only tables**, preserving everything else."""
    try:
        soup = BeautifulSoup(content, "lxml")  # Use lxml parser

        # Remove all table content
        for table in soup.find_all("table"):
            table.decompose()

        extracted_text = soup.get_text()

        # **Remove content before the first "table of contents"**
        toc_pos = extracted_text.lower().find("table of contents")
        if toc_pos != -1:
            extracted_text = extracted_text[toc_pos:]

        # **Stop at the last "Signatures" section**
        last_signature_pos = extracted_text.lower().rfind("signatures")
        if last_signature_pos != -1:
            extracted_text = extracted_text[:last_signature_pos]

        return clean_text(extracted_text)

    except Exception as e:
        print(f"⚠ Error parsing document: {e}")
        return "⚠ Parsing Error - Document could not be processed"

# Function to extract **filing date** from the text content
def extract_filing_date(content):
    """Extracts the official filing date from the SEC document."""
    match = re.search(r"CONFORMED PERIOD OF REPORT:\s*(\d{8})", content)
    if match:
        return pd.to_datetime(match.group(1), format="%Y%m%d", errors="coerce")
    return None  # Return None if no valid date is found

# Ensure output directory exists
output_dir = "extracted_sec_text"
os.makedirs(output_dir, exist_ok=True)

# Get the absolute path where files are downloaded
base_dir = os.path.abspath("sec-edgar-filings")

# Loop through each company
for company, cik in companies.items():
    print(f"Downloading filings for {company} (CIK: {cik})...")

    try:
        # Download the most recent 10-K and 10-Q reports (for the last 2 years)
        dl.get("10-K", cik)  # Annual report (Q4)
        dl.get("10-Q", cik)  # Quarterly reports (Q1, Q2, Q3)

        # Identify the correct downloaded directory
        filings_dir = os.path.join(base_dir)
        cik_str = str(cik).zfill(10)  # Ensure 10-digit CIK with leading zeros

        # Find the actual folder (should be under `sec-edgar-filings/000xxxxx/`)
        cik_folders = [f for f in os.listdir(filings_dir) if f.startswith("000") and cik_str in f]
        if not cik_folders:
            print(f"⚠ No filings found for {company} (CIK: {cik})")
            continue  # Skip if no files found

        cik_folder = os.path.join(filings_dir, cik_folders[0])  # Use first matched folder

        # Extract text from 10-K and 10-Q reports
        for form_type in ["10-K", "10-Q"]:
            form_path = os.path.join(cik_folder, form_type)

            if os.path.exists(form_path) and len(os.listdir(form_path)) > 0:
                # Loop through each downloaded filing
                for filing_folder in sorted(os.listdir(form_path), reverse=True):
                    filing_dir = os.path.join(form_path, filing_folder)

                    # Identify the correct filing file
                    filing_file = None
                    for file in os.listdir(filing_dir):
                        if file.endswith(".txt") or file.endswith(".html"):
                            filing_file = os.path.join(filing_dir, file)
                            break

                    if not filing_file:
                        continue  # Skip if no valid file found

                    # Read the filing content **ignoring encoding errors**
                    with open(filing_file, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()

                    # Extract the correct **filing date** from the document
                    reporting_date = extract_filing_date(content)

                    if reporting_date is None or pd.isnull(reporting_date) or reporting_date.year < current_year - 2:
                        print(f"⚠ Skipping outdated report for {company} ({reporting_date})...")
                        continue  # Skip old reports

                    print(f"📅 Extracted Reporting Date: {reporting_date}")

                    # Extract full textual content while **removing only tables**, **removing gibberish at the start**, and **truncating after the last "Signatures"**
                    filing_text = extract_text_without_tables(content)

                    # Determine the quarter & year from the filing date
                    quarter_info = get_quarter(reporting_date, form_type)

                    # Generate filename
                    filename = f"{company}_{quarter_info}.txt"
                    file_path = os.path.join(output_dir, filename)

                    # Save the extracted text into a .txt file
                    with open(file_path, "w", encoding="utf-8") as text_file:
                        text_file.write(filing_text)

                    print(f"Saved: {filename}")

    except Exception as e:
        print(f"Error fetching data for {company} (CIK: {cik}): {e}")

print("\nData extraction complete. All text files saved in 'extracted_sec_text' folder.")