import json
import os
import re
import oracledb

# Database connection details
user = 'ADMIN'
password = 'AISC1FinQA@2025'
dsn = 'finqadb_medium'
wallet_location = r"C:\Users\user\Downloads\Wallet_FinQADB"

# Directory containing the cleaned JSON files
data_directory = r"C:\Users\user\OneDrive - Loyalist College\AIandDS\Term 4\cleaned_data_new"

# Establish database connection
connection = oracledb.connect(
    user=user,
    password=password,
    dsn=dsn,
    config_dir=wallet_location,
    wallet_location=wallet_location,
    wallet_password=password
)
cursor = connection.cursor()

# **Reserved words in Oracle that cannot be used as column names**
ORACLE_RESERVED_WORDS = {
    "DATE", "YEAR", "TABLE", "USER", "INDEX", "SELECT", "INSERT",
    "DELETE", "UPDATE", "WHERE", "ORDER", "GROUP", "HAVING", "VALUES"
}

# **Sanitize column names to prevent SQL errors**
def sanitize_column_name(name):
    if not isinstance(name, str):
        name = str(name)  # Ensure it's a string
    
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)  # Replace invalid characters
    if name.upper() in ORACLE_RESERVED_WORDS:
        name = "D_" + name  # Prefix reserved words with "D_"
    
    if not name[0].isalpha():
        name = "C_" + name  # Ensure column starts with a letter

    return name.upper()

# **Ensure company_year_metadata table exists**
def ensure_metadata_table():
    cursor.execute("""
        SELECT COUNT(*)
        FROM USER_TABLES
        WHERE TABLE_NAME = 'COMPANY_YEAR_METADATA'
    """)
    
    if cursor.fetchone()[0] == 0:
        print("Creating company_year_metadata table...")
        cursor.execute("""
            CREATE TABLE company_year_metadata (
                id VARCHAR2(255) PRIMARY KEY,
                filename VARCHAR2(255),
                table_name VARCHAR2(255),
                company_name VARCHAR2(255),
                year NUMBER,
                record_count NUMBER,
                last_updated DATE DEFAULT SYSDATE
            )
        """)
        print("company_year_metadata table created.")


# **Create company-year table dynamically**
def create_company_year_table(table_name, columns):
    sanitized_columns = list(set(sanitize_column_name(col) for col in columns))  # Ensure unique columns
    columns_definition = ", ".join([f'"{col}" VARCHAR2(255)' for col in sanitized_columns])

    create_query = f"""
        CREATE TABLE {table_name} (
            id VARCHAR2(255),
            filename VARCHAR2(255),
            attribute VARCHAR2(255),
            {columns_definition}
        )
    """
    cursor.execute(create_query)
    print(f"Table {table_name} created with columns: {sanitized_columns}")
    return sanitized_columns

# **Ensure the company-year table exists or update it dynamically**
def verify_and_update_table(table_name, required_columns):
    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM USER_TAB_COLUMNS
        WHERE TABLE_NAME = UPPER(:table_name)
    """, {"table_name": table_name})

    existing_columns = {row[0] for row in cursor.fetchall()}
    sanitized_required_columns = {sanitize_column_name(col) for col in required_columns}

    missing_columns = sanitized_required_columns - existing_columns

    if missing_columns:
        print(f"Table {table_name} is missing columns {missing_columns}. Altering table to add them.")
        for col in missing_columns:
            cursor.execute(f'ALTER TABLE {table_name} ADD "{col}" VARCHAR2(255)')

    return list(sanitized_required_columns)

# **Insert data into company-year table**
def insert_into_company_year_table(table_name, table_ori, record_id, filename):
    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM USER_TAB_COLUMNS
        WHERE TABLE_NAME = UPPER(:table_name)
    """, {"table_name": table_name})
    existing_columns = {row[0] for row in cursor.fetchall()}

    for row in table_ori[1:]:  # Skip header row
        attribute = row[0]  # First column is the attribute
        values_dict = {}

        for col, value in zip(table_ori[0][1:], row[1:]):  # Skip first column
            sanitized_col = sanitize_column_name(col)
            if sanitized_col in existing_columns:
                values_dict[sanitized_col] = value

        insert_query = f"""
            INSERT INTO {table_name} (id, filename, attribute, {", ".join(values_dict.keys())})
            VALUES (:id, :filename, :attribute, {", ".join([f':{col}' for col in values_dict.keys()])})
        """

        values_dict["id"] = record_id
        values_dict["filename"] = filename
        values_dict["attribute"] = attribute

        cursor.execute(insert_query, values_dict)

    print(f"Data inserted into {table_name}.")

# **Insert metadata into company_year_metadata**
def insert_metadata(metadata):
    ensure_metadata_table()
    insert_query = """
        INSERT INTO company_year_metadata (id, filename, table_name, company_name, year, record_count, last_updated)
        VALUES (:id, :filename, :table_name, :company_name, :year, :record_count, SYSDATE)
    """
    cursor.execute(insert_query, metadata)
    print(f"Metadata inserted for {metadata['table_name']}.")

# **Main function to process files and insert data**
def process_files(data_directory):
    processed_companies = set()
    ensure_metadata_table()

    for file_name in os.listdir(data_directory):
        if file_name.endswith("_cleaned_data.json"):
            file_path = os.path.join(data_directory, file_name)
            with open(file_path, 'r') as f:
                data = json.load(f)

                for item in data:
                    company_name = item["filename"].split('/')[0]

                    if company_name not in processed_companies:
                        processed_companies.add(company_name)

                    if len(processed_companies) > 10:
                        print("Processed 10 companies. Stopping upload.")
                        connection.commit()
                        return

                    table_name = company_name.lower() + "_" + item["filename"].split('/')[1]
                    columns = item["table_ori"][0]  # Header row

                    cursor.execute(f"""
                        SELECT COUNT(*) FROM USER_TABLES WHERE TABLE_NAME = UPPER(:table_name)
                    """, {"table_name": table_name})
                    table_exists = cursor.fetchone()[0] > 0

                    if not table_exists:
                        sanitized_columns = create_company_year_table(table_name, columns)
                    else:
                        sanitized_columns = verify_and_update_table(table_name, columns)

                    insert_into_company_year_table(
                        table_name,
                        item["table_ori"],
                        item["id"],
                        item["filename"]
                    )

                    metadata = {
                        "id": item["id"],
                        "filename": item["filename"],
                        "table_name": table_name,
                        "company_name": company_name,
                        "year": int(item["filename"].split('/')[1]),
                        "record_count": len(item["table_ori"]) - 1
                    }
                    insert_metadata(metadata)

    connection.commit()
    print("Data inserted for 10 companies only. Upload complete.")

# **Execute the script**
process_files(data_directory)
cursor.close()
connection.close()