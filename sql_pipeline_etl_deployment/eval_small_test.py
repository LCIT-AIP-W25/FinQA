import pandas as pd
import os
import time
import oracledb
import logging
import re
import random
import httpx
from datetime import datetime
from groq import Groq

def load_excel_data(file_path):
    """Loads the Excel file and creates a dictionary of DataFrames for each company."""
    xls = pd.ExcelFile(file_path)
    company_dfs = {sheet: xls.parse(sheet) for sheet in xls.sheet_names}
    return company_dfs

def extract_sql_and_notes(llm_output):
    """Extract SQL query and additional notes from LLM output."""
    if not llm_output:
        return None, "LLM did not return any response."
    sql_match = re.search(r"SQL:\s*(.*?)(?:\nNOTE:|$)", llm_output, re.DOTALL)
    notes_match = re.search(r"NOTE:\s*(.*)", llm_output, re.DOTALL)
    query = sql_match.group(1).strip() if sql_match else None
    extra = notes_match.group(1).strip() if notes_match else "No additional notes."
    logging.debug("Extracted SQL Query: %s", query)
    logging.debug("Extracted Notes: %s", extra)
    return query, extra

def save_progress(df, model_name):
    """Saves the DataFrame after each processed row."""
    output_file = f"processed_results_{model_name}.csv"
    df.to_csv(output_file, index=False)
    logging.info("Progress saved to %s", output_file)

def query_llm(user_question, ddl_content, model_name, api_key, max_retries=5):
    """Queries the LLM API with retry logic."""
    logging.debug("Querying LLM API using model: %s", model_name)
    
    prompt = f"""
System instructions:
You are a highly intelligent and experienced SQL developer that can write precise, minimal and appropriate queries based on natural language questions.  
Based on the DDL below, generate an SQL query by deriving appropriate columns, correct filters and table names from the user query in natural language that outputs a numerical value. 

Output format:
The SQL query should ALWAYS start with "SQL:" and be the ONLY OUTPUT. For example "SQL:SELECT * FROM TABLE;".  
If you could not generate the SQL query, ONLY reply with "NOTE: [issue with creating the query].".  
ALWAYS use "" (double quotes) for table and column names.
ALWAYS use ''(single quotes) for filtering "METRICS" column.
ALWAYS prefix "ADMIN" to table names.
ALWAYS cross-check what "METRICS" filter to use by going through the insert statements in the DDL for "METRICS" column.

Information about the data:
The tables have financial data of companies. 
The column named "METRICS" in all tables just have string values of various financial metrics. 
The numerical values for a financial metric are stored inside the rest of the columns of that metric's row that contain quarterly information of that metric.
For example, Q3_2024 means Quarter 3 of 2024. 
Only extract values from "Current" column if the user specifies "current" data of a year in the input.
If the user does not specify a quarter, take all relevant quarters for the year mentioned in the user query and perform the specific operation. 
Perform the required mathematical operation in the SQL query based on what the user specified.

Examples:
User input: What was McDonald's revenue in Q3 2024?
Your output: SELECT "Q3_2024" FROM "ADMIN"."MCD_INCOME_QUARTERLY" WHERE "METRICS" = 'Revenue'; 

User input: How much gross profit did Coca-Cola report in 2023?
Your output: SELECT ("Q1_2023" + "Q2_2023" + "Q3_2023" + "Q4_2023")  FROM "ADMIN"."KO_INCOME_QUARTERLY" WHERE METRICS = 'Gross Profit';

User input: What was the ratio of quarter 3 2024 and q2 2024 for Meta's cash and equivalents?
Your output: SELECT ("Q3_2024"/"Q2_2024") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Cash and Equivalents'

ddl = \"\"\"{ddl_content}\"\"\"

## Natural Language Query
query = "{user_question}"

"""
    retries = 0
    while retries < max_retries:
        try:
            time.sleep(10)
            start_time = time.time()
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
            )
            llm_response = response.choices[0].message.content.strip()
            time_taken = round(time.time() - start_time, 2)
            logging.debug("LLM Response received: %s", llm_response)
            return llm_response, time_taken
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                retry_after = int(e.response.headers.get("retry-after", random.uniform(0, 5)))
                logging.warning("Rate limit hit. Retrying after %d seconds...", retry_after)
                time.sleep(retry_after)
                retries += 1
            else:
                logging.error("LLM API error: %s", e)
                return None, 0
    logging.error("Max retries reached. Skipping query.")
    return None, 0

def execute_sql(query, db_config):
    """Executes the SQL query and handles errors."""
    try:
        conn = oracledb.connect(
            user=db_config["user"],
            password=db_config["password"],
            dsn=db_config["dsn"],
            config_dir=db_config["wallet_location"],
            wallet_location=db_config["wallet_location"],
            wallet_password=db_config["password"]
        )
        cursor = conn.cursor()
        start_time = time.time()
        cursor.execute(query.rstrip(";"))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        execution_time = round(time.time() - start_time, 4)
        cursor.close()
        conn.close()
        return results, columns, execution_time, ""
    except oracledb.DatabaseError as e:
        logging.error("Database error: %s", e)
        return None, None, None, str(e)

def retry_query(error_msg, sql_query, ddl_content, model_name, api_key):
    """Retries generating and executing a corrected SQL query using the LLM."""
    logging.info("Retrying query due to database error: %s", error_msg)
    prompt = f"""
    
    Fix the following SQL query which resulted in an error using the DDL.
    Output format:
    The SQL query should ALWAYS start with "SQL:" and be the ONLY OUTPUT. For example "SQL:SELECT * FROM TABLE;".  
    If you could not generate the SQL query, ONLY reply with "NOTE: [issue with creating the query].".  
    ALWAYS use "" (double quotes) for table and column names.
    ALWAYS use ''(single quotes) for filtering "METRICS" column.
    ALWAYS prefix "ADMIN" to table names.
    ALWAYS cross-check what "METRICS" filter to use by going through the insert statements in the DDL for "METRICS" column.\n  
    Error message:{error_msg}\nQuery: {sql_query}\nDDL: {ddl_content}"""

    llm_output, llm_time = query_llm(prompt, ddl_content, model_name, api_key)
    if llm_output is None:
        return None, None, None, "Failed to generate corrected query."
    corrected_query, _ = extract_sql_and_notes(llm_output)
    if corrected_query:
        corrected_query = re.sub(r'("METRICS")<%=<s*([^"]+)"', r'\1 = \1\2', corrected_query)
    return corrected_query

def process_questions(company_dfs, model_name, ddl_directory, db_config, api_key):
    logging.info("Processing for model: %s", model_name)
    for company, df in company_dfs.items():
        ddl_file_path = os.path.join(ddl_directory, f"{company}_ddl.sql")
        if not os.path.exists(ddl_file_path):
            logging.warning("Skipping %s, no DDL file found.", company)
            continue
        with open(ddl_file_path, "r", encoding="utf-8") as file:
            ddl_content = file.read().strip()
        for index, row in df.iterrows():
            question = row["Question"]
            retries = 0
            while retries < 2:
                llm_output, llm_time = query_llm(question, ddl_content, model_name, api_key)
                if llm_output is None:
                    save_progress(df, model_name)
                    return  
                sql_query, _ = extract_sql_and_notes(llm_output)
                if sql_query:
                    sql_query = re.sub(r'("METRICS")<%=<s*([^"]+)"', r'\1 = \1\2', sql_query)
                results, columns, exec_time, error_msg = execute_sql(sql_query, db_config) if sql_query else (None, None, None, None)
                if error_msg:
                    logging.warning("Database error encountered. Retrying...")
                    sql_query = retry_query(error_msg, sql_query, ddl_content, model_name, api_key)
                    retries += 1
                else:
                    break
            df.at[index, "generated_query"] = sql_query or "Failed to generate query"
            df.at[index, "generated_answer"] = str(results) if results else "No results found"
            df.at[index, "time"] = exec_time if exec_time else 0
            df.at[index, "error"] = error_msg if error_msg else ''
            save_progress(df, model_name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    excel_path = "test/questions.xlsx"
    ddl_directory = "Oracle_DDLs/"
    db_config = {"user": "ADMIN", "password": "Passwordtestdb@1", "dsn": "testdb_medium","wallet_location":"Wallet_testdb"}
    api_key = "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"
    model_name = "llama-3.1-8b-instant"
    company_dfs = load_excel_data(excel_path)
    selected_companies = random.sample(list(company_dfs.keys()), min(5, len(company_dfs)))
    company_dfs = {k: company_dfs[k] for k in selected_companies}
    process_questions(company_dfs, model_name, ddl_directory, db_config, api_key)
