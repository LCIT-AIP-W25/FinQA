import streamlit as st
import oracledb
import re
import os
import pandas as pd
import logging
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

# Read the cleaned Oracle table schemas
ddl_file_path = "cleaned_oracle_table_schemas.sql"
try:
    with open(ddl_file_path, "r", encoding="utf-8") as file:
        ddl_content = file.read().strip()  # Read and remove unnecessary whitespace
except Exception as e:
    st.error("Error reading DDL file: " + str(e))
    logging.error("Error reading DDL file: %s", e)
    st.stop()

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

    # Format the query dynamically
    prompt = f"""Based on the DDL below, answer the question with an SQL query that starts with "SQL:".
For example SQL:SELECT * FROM TABLE;. Do not use any other prefix for the SQL query. 
Any extra information should be prefixed by 'NOTE:'. For example NOTE: The data requires etc.
If you do not have appropriate information, reply with "I am sorry, I am having trouble finding the right information.". All values inside "Fiscal Quarter" are in the format of QN YYYY, for example Q2 2023. 

ddl = \"\"\"{ddl_content}\"\"\"

## Natural Language Query
query = \"{user_question}\"
"""

    try:
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

        logging.debug("LLM Response received: %s", llm_response)
        return llm_response.strip()
    
    except Exception as e:
        logging.error("LLM API error: %s", e)
        st.error(f"LLM API error: {e}")
        return None

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
        return "Could not connect to Oracle.", None

    cursor = conn.cursor()
    
    try:
        logging.debug("Executing SQL Query: %s", query)
        query = query.rstrip(";")  # Remove semicolon if present
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        logging.debug("SQL Execution Successful. Rows fetched: %d", len(results))
        return results, columns

    except oracledb.DatabaseError as e:
        logging.error("SQL Execution Error: %s", e)
        return str(e), None

    finally:
        cursor.close()
        conn.close()

# Streamlit UI
st.title("💡 SQL Query Generator & Executor")
st.markdown("Enter a question, and the system will generate and execute an SQL query in Oracle.")

# User input
user_question = st.text_area("Enter your question:")

if st.button("Generate and Execute SQL"):
    if user_question:
        with st.spinner("Generating SQL Query..."):
            llm_output = query_llm(user_question)
            
            if not llm_output:
                st.error("LLM did not return any response.")
                st.stop()

            query, extra = extract_sql_and_notes(llm_output)

        if query:
            st.subheader("Generated SQL Query")
            st.code(query, language="sql")

            with st.spinner("Executing SQL Query in Oracle..."):
                results, columns = execute_sql(query)

            if columns:
                st.subheader("Query Results")
                st.dataframe(pd.DataFrame(results, columns=columns))
            else:
                st.error(f"Error executing query: {results}")

        if extra:
            st.subheader("LLM Notes")
            st.info(extra)
    else:
        st.warning("Please enter a question.")
