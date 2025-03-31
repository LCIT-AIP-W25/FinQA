import time
import logging
import re
import random
import httpx
from groq import Groq
import nltk
nltk.download('punkt_tab')


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

def query_llm(user_question, ddl_content, model_name, api_key_sql, max_retries=5, chat_history=None):
    """Queries the LLM API with retry logic."""
    logging.debug("Querying LLM API using model: %s", model_name)
    # Format last 5 messages if provided
    history_context = ""
    if chat_history:
        last_5_messages = chat_history[-5:]  # Get only the last 5 messages
        history_context = "\n\n### Conversation Context:\n"
        for msg in last_5_messages:
            speaker = "User" if msg['sender'] == 'user' else "Assistant"
            history_context += f"{speaker}: {msg['message']}\n"
    
    prompt = f"""
### Output format:
The SQL query should ALWAYS start with "SQL:". For example "SQL:SELECT * FROM TABLE;".
If you could not generate the SQL query, ONLY reply with "NOTE: [issue with creating the query].".  
ALWAYS use "" (double quotes) for table and column names.
ALWAYS use ''(single quotes) for filtering "METRICS" column.
ALWAYS prefix "ADMIN" to table names.
ALWAYS MAKE SURE THE SQL SYNTAX IS CORRECT.

### Previous Conversation Context:
{history_context} 

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
            
            client = Groq(api_key=api_key_sql)
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_completion_tokens=1024,
                top_p=1,
                stream=False,
            )
            llm_response = response.choices[0].message.content.strip()
            
            logging.debug("LLM Response received: %s", llm_response)
            return llm_response
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

