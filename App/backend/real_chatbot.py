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
import itertools

def detect_company(company_name):
    """Maps company names from user input to corresponding DDL filenames."""
    company_map = {
        "amazon": "amzn",
        "mcdonald's": "mcd",
        "meta": "meta",
        "coca-cola": "ko",
        "google": "goog",
        "alphabet": "goog",  # Google's parent company
        "s&p global": "spgi",
        "tesla": "tsla",
        "microsoft": "msft",  # Assuming you have this DDL
        "netflix": "nflx",
        "hsbc": "hsbc",
        "jpmorgan": "jpm",
        "shell": "shel",
        "att": "t",
        "verizon": "vz",
        "amd": "amd",       
        "mastercard": "ma",
        "pepsico": "pep"
    }

    # for company, ddl_prefix in company_map.items():
    #     if company.lower() in user_input.lower():
    #         return ddl_prefix  # Return the prefix for DDL filename

    # return None  # Return None if the company isn’t recognized
    return company_map.get(company_name.lower(), None)



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


def save_progress(df, model_name, mode="w"):
    """Saves the DataFrame to CSV without overwriting previous sheets."""
    output_file = f"results_{model_name}_small_test.csv"
    header = mode == "w"  # Write header only for the first sheet
    df.to_csv(output_file, mode=mode, index=False, header=header)
    logging.info("Progress saved to %s", output_file)

def query_llm(user_question, ddl_content, model_name, api_key, max_retries=5):
    """Queries the LLM API with retry logic."""
    logging.debug("Querying LLM API using model: %s", model_name)
    
    prompt = f"""
### Output format:
The SQL query should ALWAYS start with "SQL:". For example "SQL:SELECT * FROM TABLE;".
If you could not generate the SQL query, ONLY reply with "NOTE: [issue with creating the query].".  
ALWAYS use "" (double quotes) for table and column names.
ALWAYS use ''(single quotes) for filtering "METRICS" column.
ALWAYS prefix "ADMIN" to table names.
ALWAYS MAKE SURE THE SQL SYNTAX IS CORRECT.
 
### Examples:
User input: What was McDonald's revenue in Q3 2024?
Your SQL output: SELECT "Q3_2024" FROM "ADMIN"."MCD_INCOME_QUARTERLY" WHERE "METRICS" = 'Revenue';
 
User input: How much gross profit did Coca-Cola report in 2023?
Your SQL output: SELECT ("Q1_2023" + "Q2_2023" + "Q3_2023" + "Q4_2023")  FROM "ADMIN"."KO_INCOME_QUARTERLY" WHERE METRICS = 'Gross Profit';
 
User input: What was the change in operating expenses from first quarter of 2024 to the second quarter for meta?
Your SQL output: SELECT ("Q2_2024" - "Q1_2024") FROM "ADMIN"."META_INCOME_QUARTERLY" WHERE "METRICS" = 'Operating Expenses';
 
User input: What's the ratio of quarter 3 2024 and q2 2024 for Meta's cash and equivalents?
Your SQL output: SELECT ("Q3_2024"/"Q2_2024") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Cash and Equivalents'
 
User input: What is the ratio of Accounts Receivable to Total Current Assets in Q3 2024 for AMD?
or User input: What proportion of Accounts Receivable is of Total Current Assets in Q3 2024 for AMD?
Your SQL output: SELECT ar."Q3_2024" * 1.0 / tca."Q3_2024" AS ratio FROM "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" ar JOIN "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" tca ON ar."METRICS" = 'Accounts Receivable' AND tca."METRICS" = 'Total Current Assets';
 
User input: What was the average Book Value Per Share for the first three quarters of 2024 for Amazon?
Your SQL output: SELECT ("Q1_2024"+"Q2_2024"+"Q3_2024")/3 FROM "ADMIN"."AMZN_BALANCE_SHEET_QUARTERLY" where  "METRICS" = 'Book Value Per Share'
 
User input: What was the percentage change in Cash and Equivalents from Q2 2024 to Q3 2024 for amazon?
Your SQL output: SELECT ("Q3_2024"- "Q2_2024")/"Q2_2024" * 100 FROM "ADMIN"."AMZN_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Cash and Equivalents'
 
User input: Give me the minimum value of Accounts Receivable in 2023 for Meta?
Your SQL output: SELECT LEAST("Q1_2023", "Q2_2023", "Q3_2023", "Q4_2023") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Accounts Receivable'
 
User input: Provide me with the maximum value of Accounts Receivable in 2023 for Meta?
Your SQL output: SELECT GREATEST("Q1_2023", "Q2_2023", "Q3_2023", "Q4_2023") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Accounts Receivable'
 
User input: What's the year-over-year change in Retained Earnings from Q3 2023 to Q3 2024 for AMD?
Your SQL output: SELECT ("Q3_2024" - "Q3_2023") FROM "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Retained Earnings';
 
User input: How did the EPS Growth in Q3 2024 compare to Q3 2023 for Amazon?
Your SQL output: SELECT ("Q3_2024" - "Q3_2023") FROM "ADMIN"."AMZN_INCOME_QUARTERLY" WHERE "METRICS" = 'EPS Growth';
\n\n
 
### System instructions:
You generate SQL queries based on natural language questions.  
Based on the DDL below, generate an SQL query.
 
## ddl = \"\"\"{ddl_content}\"\"\"

## Natural Language Query
query = "{user_question}"
\n\n

"""
    retries = 0
    while retries < max_retries:
        try:
            time.sleep(3)
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
    Error message:{error_msg}\nQuery: {sql_query}\nDDL: {ddl_content}"""

    llm_output, llm_time = query_llm(prompt, ddl_content, model_name, api_key)
    if llm_output is None:
        return None, None, None, "Failed to generate corrected query."
    corrected_query, _ = extract_sql_and_notes(llm_output)
    if corrected_query:
        corrected_query = re.sub(r'("METRICS")<%=<s*([^"]+)"', r'\1 = \1\2', corrected_query)
    return corrected_query

def process_questions(company_dfs, ddl_directory, model_name, db_config, api_keys):
    """
    Processes questions from an Excel file, queries an LLM, and executes SQL against a database.
    
    :param excel_file_path: Path to the Excel file with questions.
    :param ddl_directory: Path to the directory containing DDL files.
    :param model_name: Name of the LLM model to use.
    :param db_config: Database configuration for SQL execution.
    :param api_keys: List of API keys to cycle through.
    """
    api_key_cycle = itertools.cycle(api_keys)
    
    first_sheet = True  # Flag to track if it's the first sheet for saving CSV
    
    for company, df in company_dfs.items():
        df["sheet_name"] = company  # Retain sheet name for each row
        
        ddl_prefix = detect_company(user_question)
        if ddl_prefix:
            ddl_file_path = os.path.join(ddl_directory, f"{ddl_prefix}_ddl.sql")
        else:
            logging.error("Company not recognized for DDL loading.")
            exit()

        if not os.path.exists(ddl_file_path):
            logging.warning("Skipping %s, no DDL file found.", company)
            continue

        with open(ddl_file_path, "r", encoding="utf-8") as file:
            ddl_content = file.read().strip()
        
        for index, row in df.iterrows():
            question = row["Question"]
            retries = 0

            while retries < 4:
                api_key = next(api_key_cycle)
                llm_output, llm_time = query_llm(question, ddl_content, model_name, api_key)

                if llm_output is None:
                    logging.warning("Skipping question due to failed LLM response.")
                    df.at[index, "generated_query"] = "Failed to generate query"
                    df.at[index, "generated_answer"] = "No results found"
                    df.at[index, "time"] = 0
                    df.at[index, "error"] = "LLM did not return a response"
                    save_progress(df.iloc[[index]], model_name, mode="w" if first_sheet else "a")  # Save row
                    continue  # Move to the next question
                
                # Extract SQL query from LLM output
                sql_query, _ = extract_sql_and_notes(llm_output)
                if sql_query:
                    sql_query = re.sub(r'("METRICS")<%=<s*([^"+])"', r'\1 = \1\2', sql_query)
                
                # Execute SQL query if available
                results, columns, exec_time, error_msg = execute_sql(sql_query, db_config) if sql_query else (None, None, None, None)

                if error_msg:
                    logging.warning("Database error encountered. Retrying...")
                    sql_query = retry_query(error_msg, sql_query, ddl_content, model_name, api_key)
                    retries += 1
                else:
                    break

            # Store results in DataFrame
            df.at[index, "generated_answer"] = str(results) if results else "No results found"
            df.at[index, "generated_query"] = sql_query or "Failed to generate query"
            df.at[index, "time"] = exec_time if exec_time else 0
            df.at[index, "error"] = error_msg if error_msg else ''

            # Save progress after every row
            save_progress(df.iloc[[index]], model_name, mode="w" if first_sheet else "a")  

        first_sheet = False  # Switch to append mode after first sheet
