import streamlit as st
import oracledb
import re
import os
import pandas as pd
import logging
import time
from groq import Groq  # Import Groq API

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Streamlit secrets
try:
    db_config = st.secrets["database"]
    llm_config = st.secrets["llm"]
except Exception as e:
    st.error("Error loading secrets: " + str(e))
    logging.error("Error loading secrets: %s", e)
    st.stop()

# Define the DDL directory
ddl_directory = "Oracle_DDLs/"

# Ensure the directory exists
if not os.path.exists(ddl_directory):
    st.error("DDL directory not found. Please ensure Oracle_ddls exists.")
    logging.error("DDL directory not found.")
    st.stop()

# List available .sql files
ddl_files = [f for f in os.listdir(ddl_directory) if f.endswith(".sql")]

if not ddl_files:
    st.error("No DDL files found in Oracle_ddls.")
    logging.error("No DDL files found in Oracle_ddls.")
    st.stop()

# Streamlit UI
st.title("💡 SQL Query Generator & Executor")

# Dropdown for selecting DDL file
selected_ddl_file = st.selectbox("Select a table schema file:", ddl_files)

# Load the selected DDL file
ddl_file_path = os.path.join(ddl_directory, selected_ddl_file)
try:
    with open(ddl_file_path, "r", encoding="utf-8") as file:
        ddl_content = file.read().strip()  # Read and remove unnecessary whitespace
except Exception as e:
    st.error("Error reading DDL file: " + str(e))
    logging.error("Error reading DDL file: %s", e)
    st.stop()

st.markdown(f"### Using schema from `{selected_ddl_file}`")

# Initialize Oracle connection
def connect_to_oracle():
    try:
        logging.debug("Connecting to Oracle Database...")
        conn = oracledb.connect(
            user=db_config["user"],
            password=db_config["password"],
            dsn=db_config["dsn"],
            config_dir=db_config["wallet_location"],
            wallet_location=db_config["wallet_location"],
            wallet_password=db_config["password"]
        )
        logging.debug("Oracle connection successful.")
        return conn
    except oracledb.DatabaseError as e:
        logging.error("Oracle connection error: %s", e)
        st.error(f"Oracle connection error: {e}")
        return None

# Query Groq API
def query_llm(user_question):
    logging.debug("Querying LLM API...")
    
    prompt = f"""
You are a highly intelligent and experienced SQL developer that can write precise, minimal and appropriate queries based on natural language questions. 
Based on the DDL below, derive appropriate metrics, the correct quarter/year and the table name from the user query.The  DDL also includes the value inside metrics column of each table through an insert statement, so always cross check what the user requires.
Answer the question with an SQL query that starts with "SQL:".For example SQL:SELECT * FROM TABLE;. 
Do not use any other prefix for the SQL query and only provide it if you find the exact information in the provided DDL. 
Each column named metric in every table just has the textual name of the metric, and the numerical values for that metric are stored inside the rest of the columns of that row which have quraterly information of that metric
For example Q3_2024 means Quarter 3 of 2024, but Q3_2024 is stored as a string in the database.
ALWAYS use single quotes just while filtering the metrics column. ALWAYS use "" for table names in the SQL query. Use the correct format of the metrics column by matching it with the DDL file of the table, for example, if the column is "Metrics" use "Metrics" in the SQL query, if the column is formatted like "METRICS", use "METRICS". 
ANY column in a table that starts with Current followed by a year is a representation of data for that year, it is not a metric, neither it is quarterly data. Only extract values from this column if the user specifies "current" data of a year in a the input.
If a numerical value of a quarter/year's metric is asked, the SQL query should be designed in a way that just outputs the numerical answer. 
If the query asks for yearly data, remember to perform the specific operation for all quarters of the year/s.
Explain how you derived the SQL query by prefixing it with 'NOTE:'. 
NEVER reveal any sensitive information about the database including table names, use placeholder terms instead. For example NOTE: The query requires etc. 
ANY other information other than the SQL query should also be prefixed by NOTE:.
If you did not find appropriate metrics in the DDL, ONLY reply with "I am sorry, I am having trouble finding the right information.". 

ddl = \"\"\"{ddl_content}\"\"\"

## Natural Language Query
query = \"{user_question}\"
"""

    try:
        start_time = time.time()
        client = Groq(api_key=llm_config["api_key"])
        completion = client.chat.completions.create(
            model=llm_config["model"],
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        llm_response = ""
        for chunk in completion:
            if hasattr(chunk.choices[0].delta, "content"):
                llm_response += chunk.choices[0].delta.content or ""

        end_time = time.time()
        time_taken = round(end_time - start_time, 2)

        logging.debug("LLM Response received: %s", llm_response)
        return llm_response.strip(), time_taken
    
    except Exception as e:
        logging.error("LLM API error: %s", e)
        st.error(f"LLM API error: {e}")
        return None, 0

# Extract SQL and extra notes
def extract_sql_and_notes(llm_output):
    if not llm_output:
        return None, "LLM did not return any response."

    sql_match = re.search(r"SQL:\s*(.*?)(?:\nNOTE:|$)", llm_output, re.DOTALL)
    notes_match = re.search(r"NOTE:\s*(.*)", llm_output, re.DOTALL)

    query = sql_match.group(1).strip() if sql_match else None
    extra = notes_match.group(1).strip() if notes_match else "No additional notes."
    
    logging.debug("Extracted SQL Query: %s", query)
    logging.debug("Extracted Notes: %s", extra)
    
    return query, extra

# Execute SQL query in Oracle
def execute_sql(query):
    conn = connect_to_oracle()
    if not conn:
        return "Could not connect to Oracle.", None, 0

    cursor = conn.cursor()
    
    try:
        start_time = time.time()
        logging.debug("Executing SQL Query: %s", query)
        query = query.rstrip(";")  # Remove semicolon if present
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)

        logging.debug("SQL Execution Successful. Rows fetched: %d", len(results))
        return results, columns, execution_time

    except oracledb.DatabaseError as e:
        logging.error("SQL Execution Error: %s", e)
        return str(e), None, 0

    finally:
        cursor.close()
        conn.close()

# User input
user_question = st.text_area("Enter your question:")

if st.button("Generate and Execute SQL"):
    if user_question:
        llm_output, time_taken = query_llm(user_question)
        if not llm_output:
            st.error("LLM did not return any response.")
            st.stop()

        query, extra = extract_sql_and_notes(llm_output)

        if query:
            st.subheader("Generated SQL Query")
            st.text_area("SQL Output:", value=query, height=100)

            results, columns, execution_time = execute_sql(query)
            if columns and results:
                # Extract the first numerical value and display it
                output_value = str(results[0][1]) if len(results[0]) > 1 else str(results[0][0])
                st.text_area("Query Result:", value=output_value, height=70)
            else:
                st.text_area("Query Result:", value="No valid results found.", height=70)

            st.write(f"⏱ **Time Taken:** {round(time_taken + execution_time, 2)} seconds")

        if extra:
            st.text_area("LLM Notes:", value=extra, height=100)
    else:
        st.warning("Please enter a question.")
