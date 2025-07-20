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
    "COCA COLA": "KO",
    "JPMORGAN": "JPM",
    "NETFLIX": "NFLX",
    "AMD": "AMD",
    "VISA": "V",
    "MASTERCARD": "MA",
    "PEPSICO": "PEP",
    "VERIZON": "VZ",
    "AT&T": "T",
    "MCDONALDS": "MCD",
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
        # Attempt to extract specific dates
    start_date, end_date = extract_explicit_date_range(user_question)

    if start_date and end_date:
        user_question += f" Use date BETWEEN '{start_date}' AND '{end_date}'"

    """
    Generates SQL query for stock price lookup based on user question.
    """
    prompt = f"""
### Instructions:
You are a financial SQL assistant.
Generate a valid SQL query to retrieve stock price data from a PostgreSQL table called "stock_data".
The table has the following columns: ticker, date, open, high, low, close.

Rules:
- Always filter by ticker: WHERE ticker = '{company_ticker}'
- Parse the date or range: use `=` for specific date or `BETWEEN` for ranges
- If user asks for latest: use ORDER BY date DESC LIMIT 1
- If the user asks for average, max, or min — use AVG(), MAX(), or MIN()
- Only return the required columns (open, close, or all)
- Prefix your query with `SQL:` and ensure it's valid PostgreSQL

### Examples:
Q: What was the stock price for TSLA on March 3, 2023?  
SQL: SELECT date, open, high, low, close FROM stock_data WHERE ticker = 'TSLA' AND date = '2023-03-03';

Q: What was the stock price for NFLX in 2022?  
SQL: SELECT date, open, high, low, close FROM stock_data WHERE ticker = 'NFLX' AND date BETWEEN '2022-01-01' AND '2022-12-31' ORDER BY date ASC LIMIT 1;

Q: What is the average closing price for AMZN in 2021?  
SQL: SELECT AVG(close) FROM stock_data WHERE ticker = 'AMZN' AND date BETWEEN '2021-01-01' AND '2021-12-31';

Q: What was the highest high price for META in 2020?  
SQL: SELECT MAX(high) FROM stock_data WHERE ticker = 'META' AND date BETWEEN '2020-01-01' AND '2020-12-31';

Q: Show me just the opening price of KO on Jan 10, 2023?  
SQL: SELECT open FROM stock_data WHERE ticker = 'KO' AND date = '2023-01-10';

Q: What is the latest stock price for JPM?  
SQL: SELECT date, open, high, low, close FROM stock_data WHERE ticker = 'JPM' ORDER BY date DESC LIMIT 1;

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

        # Extract SQL query from result
        match = re.search(r"SQL:\s*(SELECT.*?);?(?:\n|$)", result, re.DOTALL | re.IGNORECASE)
        if match:
            query = match.group(1).strip().rstrip(";")
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

def fetch_stock_price_llm(user_question, company_name):
    # Step 1: Generate SQL query using Groq LLM
     # Convert full company name to ticker
    company_ticker = COMPANY_TICKER_MAP.get(company_name.upper())

    if not company_ticker:
        return f"❌ Unknown company: {company_name}. Please enter a valid company name."
    query = generate_stock_sql_query(user_question, company_ticker)
    if not query:
        return "❌ Failed to generate a SQL query. Please try rephrasing your question."

    try:
        # Step 2: Run query against PostgreSQL
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                # Remove leading 'SQL:' if present
                clean_query = query.replace("SQL:", "").strip()
                cursor.execute(clean_query)
                print("\n📝 Debug Log")
                print(f"🔎 User Question: {user_question}")
                print(f"🧠 Generated SQL: {query}")
                row = cursor.fetchone()
                print(f"📤 Output Row: {row}")
                if row:
                    columns = [desc[0] for desc in cursor.description]  # Get column names from cursor
                    monetary_columns = {"open", "close", "high", "low", "avg", "min", "max"}

                    result_parts = [f"{col.capitalize()}: {'$' + str(round(val, 2)) + ' million' if col.lower() in monetary_columns and isinstance(val, (float, int)) else val}" for col, val in zip(columns, row)]

                    return f"📊 Result for **{company_ticker}** based on your query:\n" + "\n".join(f"• {part}" for part in result_parts)
                else:
                    return f"⚠️ No stock data found for {company_ticker} on that date."
    except Exception as e:
        return f"❌ Database error: {e}"