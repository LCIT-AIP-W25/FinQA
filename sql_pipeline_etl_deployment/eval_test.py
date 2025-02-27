
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

# Configure logging to save logs to a file
log_file = "sql_pipeline_etl_deployment.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Save logs to a file
        logging.StreamHandler()        # Print logs to the console
    ]
)

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
NEVER CREATE YOUR OWN COLUMN OR FILTERS FOR METRICS COLUMN, ONLY USE EXACTLY WHAT IS PROVIDED IN THE DDL.
IF THE USER ONLY MENTIONS AN YEAR BUT DOES NOT SPECIFY A QUARTER, TAKE ALL EXISTING QUARTERS PRESENT IN THE DDL FOR THE YEAR MENTIONED IN THE USER QUERY AND PERFORM THE SPECIFIC OPERATION.
ALWAYS cross-check what "METRICS" filter to use by going through the insert statements in the DDL for "METRICS" column.

### Information about the data:
The tables have quarterly financial data of companies, where each column represents quarterly information of a metric.
The column named "METRICS" in all tables just have string values of various financial metrics. 
The numerical values for a financial metric are stored inside the rest of the columns of that metric's row that contain quarterly information of that metric.
For example, Q3_2024 means Quarter 3 of 2024.
Only extract values from "Current" column if the user specifies "current" data of a year in the input.

### Examples:
User input: What was McDonald's revenue in Q3 2024?
Your SQL output: SELECT "Q3_2024" FROM "ADMIN"."MCD_INCOME_QUARTERLY" WHERE "METRICS" = 'Revenue'; 

User input: How much gross profit did Coca-Cola report in 2023?
Your SQL output: SELECT ("Q1_2023" + "Q2_2023" + "Q3_2023" + "Q4_2023")  FROM "ADMIN"."KO_INCOME_QUARTERLY" WHERE METRICS = 'Gross Profit';

User input: What was the change in operating expenses from first quarter of 2024 to the second quarter for meta?
Your SQL output: SELECT ("Q2_2024" - "Q1_2024") FROM "ADMIN"."META_INCOME_QUARTERLY" WHERE "METRICS" = 'Operating Expenses';

User input: What was the ratio of quarter 3 2024 and q2 2024 for Meta's cash and equivalents?
Your SQL output: SELECT ("Q3_2024"/"Q2_2024") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Cash and Equivalents'

User input: What is the ratio of Accounts Receivable to Total Current Assets in Q3 2024 for AMD?
Your SQL output: SELECT ar."Q3_2024" * 1.0 / tca."Q3_2024" AS ratio FROM "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" ar JOIN "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" tca ON ar."METRICS" = 'Accounts Receivable' AND tca."METRICS" = 'Total Current Assets';

User input: What proportion of Accounts Receivable is of Total Current Assets in Q3 2024 for AMD?
Your SQL output: SELECT ar."Q3_2024" * 1.0 / tca."Q3_2024" AS ratio FROM "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" ar JOIN "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" tca ON ar."METRICS" = 'Accounts Receivable' AND tca."METRICS" = 'Total Current Assets';

User input: What was the average Book Value Per Share for the first three quarters of 2024 for Amazon?
Your SQL output: SELECT ("Q1_2024"+"Q2_2024"+"Q3_2024")/3 FROM "ADMIN"."AMZN_BALANCE_SHEET_QUARTERLY" where  "METRICS" = 'Book Value Per Share'

User input: What was the percentage change in Cash and Equivalents from Q2 2024 to Q3 2024 for amazon?
Your SQL output: SELECT ("Q3_2024"- "Q2_2024")/"Q2_2024" * 100 FROM "ADMIN"."AMZN_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Cash and Equivalents' 

User input: What is the minimum value of Accounts Receivable in 2023 for Meta?
Your SQL output: SELECT LEAST("Q1_2023", "Q2_2023", "Q3_2023", "Q4_2023") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Accounts Receivable'

User input: What is the maximum value of Accounts Receivable in 2023 for Meta?
Your SQL output: SELECT GREATEST("Q1_2023", "Q2_2023", "Q3_2023", "Q4_2023") FROM "ADMIN"."META_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Accounts Receivable'

User input: What is the year-over-year change in Retained Earnings from Q3 2023 to Q3 2024 for AMD?
Your SQL output: SELECT ("Q3_2024" - "Q3_2023") FROM "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" WHERE "METRICS" = 'Retained Earnings';

User input: How did the EPS Growth in Q3 2024 compare to Q3 2023 for Amazon?
Your SQL output: SELECT ("Q3_2024" - "Q3_2023") FROM "ADMIN"."AMZN_INCOME_QUARTERLY" WHERE "METRICS" = 'EPS Growth';
\n\n

### System instructions:
You generate SQL queries based on natural language questions.  
Based on the DDL below, generate an SQL query by deriving correct columns, filters and table names that outputs a numerical value. 

## Natural Language Query
query = "{user_question}"
\n\n
## ddl = \"\"\"{ddl_content}\"\"\"


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
                max_completion_tokens=512,
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
    api_key_cycle = itertools.cycle(api_keys)
    progress_df = pd.DataFrame(columns=["sheet_name", "Question", "Answer", "generated_answer", "generated_query", "time", "error"])
    output_file = f"results_{model_name}_evaluation.csv"

    for company, df in company_dfs.items():
        logging.info(f"Processing sheet: {company}")
        df["sheet_name"] = company

        ddl_file_path = os.path.join(ddl_directory, f"{company}_ddl.sql")
        if not os.path.exists(ddl_file_path):
            logging.warning("Skipping %s, no DDL file found.", company)
            continue

        with open(ddl_file_path, "r", encoding="utf-8") as file:
            ddl_content = file.read().strip()

        for index, row in df.iterrows():
            logging.info(f"Processing question {index + 1} from sheet {company}")
            question = row["Question"]
            answer = row.get("Answer", "N/A")  # Get original answer if available, else "N/A"
            retries = 0

            while retries < 4:
                api_key = next(api_key_cycle)
                llm_output, llm_time = query_llm(question, ddl_content, model_name, api_key)

                if llm_output is None:
                    logging.warning("Skipping question due to failed LLM response.")
                    row_data = {
                        "sheet_name": company,
                        "Question": question,
                        "Answer": answer,
                        "generated_answer": "No results found",
                        "generated_query": "Failed to generate query",
                        "time": 0,
                        "error": "LLM did not return a response"
                    }
                    progress_df = pd.concat([progress_df, pd.DataFrame([row_data])], ignore_index=True)
                    break

                sql_query, _ = extract_sql_and_notes(llm_output)
                if sql_query:
                    sql_query = re.sub(r'("METRICS")<%=<s*([^"+])"', r'\1 = \1\2', sql_query)

                results, columns, exec_time, error_msg = execute_sql(sql_query, db_config) if sql_query else (None, None, None, None)

                if error_msg:
                    logging.warning("Database error encountered. Retrying...")
                    sql_query = retry_query(error_msg, sql_query, ddl_content, model_name, api_key)
                    retries += 1
                else:
                    break

            row_data = {
                "sheet_name": company,
                "Question": question,
                "Answer": answer,
                "generated_answer": str(results) if results else "No results found",
                "generated_query": sql_query or "Failed to generate query",
                "time": exec_time if exec_time else 0,
                "error": error_msg if error_msg else ''
            }
            progress_df = pd.concat([progress_df, pd.DataFrame([row_data])], ignore_index=True)

        progress_df.to_csv(output_file, mode="w", index=False)
        logging.info(f"Progress saved to {output_file}")

    progress_df.to_csv(output_file, mode="w", index=False)
    logging.info(f"Final results saved to {output_file}")

if __name__ == "__main__":
    excel_path = "test/questions.xlsx"
    ddl_directory = "Oracle_DDLs/"
    db_config = {"user": "ADMIN", "password": "Passwordtestdb@1", "dsn": "testdb_medium", "wallet_location": "Wallet_testdb"}
    api_keys = [
        "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",
        "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",
        "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",
        "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",
        "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",
        "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",
        "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",
        "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"
        
    ]
    model_name = "llama-3.3-70b-versatile"
    company_dfs = load_excel_data(excel_path)
    process_questions(company_dfs, ddl_directory, model_name, db_config, api_keys)