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

def query_llm(user_question, ddl_content, model_name, api_key, max_retries=5):
    """Queries the LLM to generate an SQL query based on the user's question with retry logic, rate limiting, and delay."""
    logging.debug("Querying LLM API using model: %s", model_name)
    
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
query = "{user_question}"


"""
    
    retries = 0
    while retries < max_retries:
        try:
            time.sleep(random.uniform(0.5, 1))  # Adding a random delay between 0.5s and 1s
            start_time = time.time()
            client = Groq(api_key=api_key)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
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
                logging.warning(f"Rate limit hit. Retrying after {retry_after} seconds...")
                time.sleep(retry_after)
                retries += 1
            else:
                logging.error("LLM API error: %s", e)
                return None, 0
    logging.error("Max retries reached. Skipping query.")
    return None, 0

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

def execute_sql(query, db_config):
    """Executes the SQL query using OracleDB and captures errors."""
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

def process_questions(company_dfs, models, ddl_directory, db_config, api_key):
    """Processes questions for each company using different models."""
    for model_name in models:
        logging.info("Processing for model: %s", model_name)
        for company, df in company_dfs.items():
            ddl_file_path = os.path.join(ddl_directory, f"{company}_ddl.sql")
            if not os.path.exists(ddl_file_path):
                logging.warning("Skipping %s, no DDL file found.", company)
                continue
            
            with open(ddl_file_path, "r", encoding="utf-8") as file:
                ddl_content = file.read().strip()
            
            generated_answers, sql_queries, execution_times, error_msgs = [], [], [], []
            for question in df["Question"]:
                llm_output, llm_time = query_llm(question, ddl_content, model_name, api_key)
                sql_query, _ = extract_sql_and_notes(llm_output)
                results, columns, exec_time, error_msg = execute_sql(sql_query, db_config) if sql_query else (None, None, None, None)
                generated_answers.append(str(results) if results else "No results found")
                sql_queries.append(sql_query or "Failed to generate query")
                execution_times.append(exec_time if exec_time else 0)
                error_msgs.append(error_msg if error_msg else '')
            
            df["generated_query"] = sql_queries
            df["generated_answer"] = generated_answers
            df["time"] = execution_times
            df["error"] = error_msgs
            
        merged_df = pd.concat(company_dfs.values(), ignore_index=True)
        output_file = f"processed_results_{model_name}.csv"
        merged_df.to_csv(output_file, index=False)
        logging.info("Saved results to %s", output_file)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    
    excel_path = "test/QAData.xlsx"
    ddl_directory = "Oracle_DDLs/"

    db_config = {"user": "ADMIN", "password": "Passwordtestdb@1", "dsn": "testdb_medium","wallet_location":"Wallet_testdb"}
    api_key = "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"
    models = ["llama-3.1-8b-instant","mixtral-8x7b-32768", "qwen-2.5-32b", "gemma2-9b-it"]
    
    company_dfs = load_excel_data(excel_path)
    selected_companies = random.sample(list(company_dfs.keys()), min(3, len(company_dfs)))
    company_dfs = {k: company_dfs[k] for k in selected_companies}
    process_questions(company_dfs, models, ddl_directory, db_config, api_key)
