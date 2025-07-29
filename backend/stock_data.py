# generate_stock_sql.py
import re
import time
import psycopg2
from groq import Groq
import os
from dotenv import load_dotenv
import dateparser
from datetime import datetime

# backend/company_mapping.py

COMPANY_TICKER_MAP = {
    "GOOGLE": "GOOG",
    "AMAZON": "AMZN",
    "TESLA": "TSLA",
    "META": "META",
    "APPLE": "AAPL",
    "MICROSOFT": "MSFT",
    "JP MORGAN": "JPM",
    "NETFLIX": "NFLX",
    "AMD": "AMD",
    "VISA": "V",
    "MASTERCARD": "MA",
    "PEPSICO": "PEP",
    "AT&T": "T",
    "MCDONALD": "MCD",
    "S&P GLOBAL": "SPGI"
}


def extract_explicit_date_range(user_question):
    """
    Parses the user question to find explicit or relative dates.
    Returns (start_date, end_date) if found, else (None, None)
    """
    # Try detecting a specific day
    parsed_date = dateparser.parse(user_question)
    if parsed_date:
        date_str = parsed_date.strftime("%Y-%m-%d")
        return date_str, date_str

    # Try detecting ranges like "last week", "past month", etc.
    # (can extend logic here as needed)
    return None, None



load_dotenv()  # Load the .env file
# Initialize Groq Client

client = Groq(api_key=os.getenv("GROQ_API_STOCK"))
 # Replace with your actual key or pass dynamically

def generate_stock_sql_query(user_question, company_ticker, model_name="llama3-70b-8192"):
    start_date, end_date = extract_explicit_date_range(user_question)

    if start_date and end_date:
        user_question += f" Use date BETWEEN '{start_date}' AND '{end_date}'"

    if not re.search(r"(open|close|high|low|average|price)", user_question, re.IGNORECASE):
        user_question += " average closing price"

    if not re.search(r"\d{4}", user_question):
        user_question += " for the last available year"

    prompt = f"""
### Instructions:
You are a financial SQL assistant.
Generate a valid SQL query to retrieve stock price data from a PostgreSQL table called "stock_data".
The table has the following columns: ticker, date, open, high, low, close.

### Key Rules:
- Always filter by ticker: WHERE ticker = '{company_ticker}'
- Use exact dates like 'YYYY-MM-DD' or BETWEEN ranges for year/month
- Use ORDER BY date DESC LIMIT 1 for latest price
- Use subqueries for comparisons (e.g., percentage/difference between years)
- Do not include explanations or comments — return only the raw SQL
- When comparing stock prices between years, use the latest available trading date within that year
- When calculating percentage change across years (e.g., close/high/low/open), use the latest available trading day in each year, not a fixed date like '2015-12-31'.
- Always use ROUND(..., 2) and handle potential division by zero with NULLIF.

### Examples:
User: What was the stock price for TSLA on March 3, 2023?  
SQL: SELECT date, open, high, low, close FROM stock_data WHERE ticker = 'TSLA' AND date = '2023-03-03';

User: What is the average closing price for AMZN in 2021?  
SQL: SELECT AVG(close) FROM stock_data WHERE ticker = 'AMZN' AND date BETWEEN '2021-01-01' AND '2021-12-31';

User: What is the difference in close price between 2015 and 2016 for TSLA?
SQL: SELECT (close_2016 - close_2015) AS price_difference FROM (
    SELECT
        MAX(CASE WHEN date = (SELECT MAX(date) FROM stock_data WHERE ticker = 'JPM' AND date BETWEEN '2015-01-01' AND '2015-12-31') THEN close END) AS close_2015,
        MAX(CASE WHEN date = (SELECT MAX(date) FROM stock_data WHERE ticker = 'JPM' AND date BETWEEN '2016-01-01' AND '2016-12-31') THEN close END) AS close_2016
    FROM stock_data
    WHERE ticker = 'TSLA'
) AS yearly_prices;

User: What is the percentage change in close price between 2018 and 2022 for JPM?
SQL: SELECT 
  ROUND(
    ((avg_2019 - avg_2018) / NULLIF(avg_2018, 0))::numeric * 100, 2
  ) AS percentage_change
FROM (
  SELECT
    AVG(CASE WHEN date BETWEEN '2018-01-01' AND '2018-12-31' THEN close END) AS avg_2018,
    AVG(CASE WHEN date BETWEEN '2019-01-01' AND '2019-12-31' THEN close END) AS avg_2019
  FROM stock_data
  WHERE ticker = 'AMD'
) AS yearly_avg;






### User Question:
{user_question}
"""

    try:
        print("\n🔍 Sending prompt to Groq to generate SQL...")
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=256
        )

        result = response.choices[0].message.content.strip()

        # Extract SQL query from model output
        match = re.search(r"SELECT\s.*?FROM.*", result, re.IGNORECASE | re.DOTALL)
        if match:
            query = match.group(0).strip().rstrip(";")
            print("✅ SQL generated:", query)
            return query
        else:
            print("⚠️ Failed to extract SQL query from LLM response.")
            return None

    except Exception as e:
        print(f"❌ Error generating SQL: {e}")
        return None


DB_CONFIG = {
    "host": "aws-0-ca-central-1.pooler.supabase.com",
    "port": "5432",
    "database": "postgres",
    "user": "postgres.ukepmwoqxybhauovasry",
    "password": "FinAnswer@Loyalist"
}

def fetch_stock_price_llm(user_question, company_ticker):
    """
    Handles LLM-driven stock query generation and executes it on PostgreSQL.
    Assumes company_ticker is already normalized (e.g., 'TSLA', 'AAPL').
    """
    query = generate_stock_sql_query(user_question, company_ticker)
    
    if not query:
        return "❌ Failed to generate a SQL query. Please try rephrasing your question."

    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()

        if not result:
            return "⚠️ No data found for the given stock query."

        return "\n".join(" | ".join(str(cell) for cell in row) for row in result)

    except Exception as e:
        return f"❌ Error executing SQL query: {str(e)}"
