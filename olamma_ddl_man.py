import time
import ollama
import mysql.connector
import streamlit as st

# 📌 Manually define the DDL of your table
DDL_INFO = """
CREATE TABLE table1 (
    Metrics VARCHAR(255) NOT NULL CHECK (
        Metrics IN ('Cash & Equivalents', 'Short-Term Investments', 'Cash & Short-Term Investments', 'Cash Growth', 
                    'Accounts Receivable', 'Other Receivables', 'Receivables', 'Inventory', 'Restricted Cash', 
                    'Other Current Assets', 'Total Current Assets', 'Property, Plant & Equipment', 'Long-Term Investments', 
                    'Long-Term Deferred Tax Assets', 'Other Long-Term Assets', 'Total Assets', 'Accounts Payable', 
                    'Short-Term Debt', 'Current Portion of Long-Term Debt', 'Current Portion of Leases', 
                    'Current Income Taxes Payable', 'Current Unearned Revenue', 'Other Current Liabilities', 
                    'Total Current Liabilities', 'Long-Term Debt', 'Long-Term Leases', 'Other Long-Term Liabilities', 
                    'Total Liabilities', 'Common Stock', 'Retained Earnings', 'Comprehensive Income & Other', 
                    'Shareholders\' Equity', 'Total Liabilities & Equity', 'Total Debt', 'Net Cash (Debt)', 'Net Cash Growth', 
                    'Net Cash Per Share', 'Filing Date Shares Outstanding', 'Total Common Shares Outstanding', 'Working Capital', 
                    'Book Value Per Share', 'Tangible Book Value', 'Tangible Book Value Per Share', 'Land', 'Machinery', 
                    'Leasehold Improvements')
    ) COMMENT 'Categorical column: Filters specific financial metrics',
    
    Q4_2024 DECIMAL(15,4),    Q3_2024 DECIMAL(15,4),    Q2_2024 DECIMAL(15,4),    Q1_2024 DECIMAL(15,4),
    Q4_2023 DECIMAL(15,4),    Q3_2023 DECIMAL(15,4),    Q2_2023 DECIMAL(15,4),    Q1_2023 DECIMAL(15,4), PRIMARY KEY (Metrics)
);

CREATE TABLE table2 (
    Metrics VARCHAR(255) NOT NULL CHECK (
        Metrics IN ('Net Income', 'Depreciation & Amortization', 'Stock-Based Compensation', 'Other Operating Activities',
                    'Change in Accounts Receivable', 'Change in Inventory', 'Change in Accounts Payable', 'Change in Unearned Revenue',
                    'Change in Other Net Operating Assets', 'Operating Cash Flow', 'Operating Cash Flow Growth',
                    'Capital Expenditures', 'Cash Acquisitions', 'Investment in Securities', 'Other Investing Activities',
                    'Investing Cash Flow', 'Short-Term Debt Issued', 'Long-Term Debt Issued', 'Total Debt Issued',
                    'Short-Term Debt Repaid', 'Long-Term Debt Repaid', 'Total Debt Repaid', 'Net Debt Issued (Repaid)',
                    'Issuance of Common Stock', 'Repurchase of Common Stock', 'Common Dividends Paid',
                    'Other Financing Activities', 'Financing Cash Flow', 'Net Cash Flow', 'Free Cash Flow',
                    'Free Cash Flow Growth', 'Free Cash Flow Margin', 'Free Cash Flow Per Share',
                    'Cash Interest Paid', 'Cash Income Tax Paid', 'Levered Free Cash Flow', 'Unlevered Free Cash Flow',
                    'Change in Net Working Capital')
    ) COMMENT 'Categorical column: Filters specific financial metrics',
    
    Q4_2024 DECIMAL(15,4),    Q3_2024 DECIMAL(15,4),    Q2_2024 DECIMAL(15,4),    Q1_2024 DECIMAL(15,4),
    Q4_2023 DECIMAL(15,4),    Q3_2023 DECIMAL(15,4),    Q2_2023 DECIMAL(15,4),    Q1_2023 DECIMAL(15,4), PRIMARY KEY (Metrics)
);

CREATE TABLE table3 (
    Metrics VARCHAR(255) CHECK (Metrics IN (
        'Market Capitalization', 'Market Cap Growth', 'Enterprise Value', 'Last Close Price', 'PE Ratio', 'Forward PE',
        'PS Ratio', 'PB Ratio', 'P/TBV Ratio', 'P/FCF Ratio', 'P/OCF Ratio', 'PEG Ratio', 'EV/Sales Ratio',
        'EV/EBITDA Ratio', 'EV/EBIT Ratio', 'EV/FCF Ratio', 'Debt / Equity Ratio', 'Debt / EBITDA Ratio',
        'Debt / FCF Ratio', 'Asset Turnover', 'Inventory Turnover', 'Quick Ratio', 'Current Ratio',
        'Return on Equity (ROE)', 'Return on Assets (ROA)', 'Return on Capital (ROIC)', 'Earnings Yield',
        'FCF Yield', 'Dividend Yield', 'Payout Ratio', 'Buyback Yield / Dilution', 'Total Shareholder Return'
    )),
    Q4_2024 DECIMAL(15,4),    Q3_2024 DECIMAL(15,4),    Q2_2024 DECIMAL(15,4),    Q1_2024 DECIMAL(15,4),
    Q4_2023 DECIMAL(15,4),    Q3_2023 DECIMAL(15,4),    Q2_2023 DECIMAL(15,4),    Q1_2023 DECIMAL(15,4), PRIMARY KEY (Metrics)
);

CREATE TABLE table4 (
    Metrics VARCHAR(255) CHECK (Metrics IN (
        'Revenue', 'Revenue Growth (YoY)', 'Cost of Revenue', 'Gross Profit', 
        'Selling, General & Admin', 'Research & Development', 'Operating Expenses', 
        'Operating Income', 'Interest Expense', 'Interest & Investment Income', 
        'Currency Exchange Gain (Loss)', 'Other Non Operating Income (Expenses)', 
        'EBT Excluding Unusual Items', 'Gain (Loss) on Sale of Investments', 'Pretax Income', 
        'Income Tax Expense', 'Net Income', 'Net Income to Common', 'Net Income Growth', 
        'Shares Outstanding (Basic)', 'Shares Outstanding (Diluted)', 'Shares Change (YoY)', 
        'EPS (Basic)', 'EPS (Diluted)', 'EPS Growth', 'Free Cash Flow', 'Free Cash Flow Per Share', 
        'Dividend Per Share', 'Dividend Growth', 'Gross Margin', 'Operating Margin', 'Profit Margin', 
        'Free Cash Flow Margin', 'EBITDA', 'EBITDA Margin', 'D&A For EBITDA', 'EBIT', 
        'EBIT Margin', 'Effective Tax Rate', 'Revenue as Reported'
    )),
    Q4_2024 DECIMAL(15,4),    Q3_2024 DECIMAL(15,4),    Q2_2024 DECIMAL(15,4),    Q1_2024 DECIMAL(15,4),
    Q4_2023 DECIMAL(15,4),    Q3_2023 DECIMAL(15,4),    Q2_2023 DECIMAL(15,4),    Q1_2023 DECIMAL(15,4), PRIMARY KEY (Metrics)
);
"""

# 📌 Function to generate SQL using predefined DDL
def generate_sql(question, ddl_info=DDL_INFO):
    prompt = f"""
    Convert this natural language question into a simple and efficient SQL query.
    
    Use the following database schema:
    
    {ddl_info}
    
    Ensure:
    - The SQL query is fully correct and executable.
    - If complex, break it down using CTEs (WITH clauses) or subqueries for better readability.
    - Optimize joins and filters efficiently.
    - If aggregations are involved, group by the necessary columns.
    - Ensure column names match exactly as in the schema.

    Question: {question}
    SQL Query:
    """
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# 📌 Function to connect to MySQL
# def connect_to_db():
#     conn = mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="root",
#         database="ollama_server"
#     )
#     return conn

# 📌 Function to execute SQL query
# def execute_query(conn, sql_query):
#     cursor = conn.cursor()
#     cursor.execute(sql_query)
#     return cursor.fetchall()

# ========================== UI USING STREAMLIT ==========================
st.title("🧠 Natural Language to SQL Query Generator")
st.write("Enter your question in natural language, generate an SQL query?")

# 🔍 User Input for Natural Language Question
question = st.text_input("❓ Enter your question:")

# ✅ Generate SQL Query
if st.button("🔍 Generate SQL Query"):
    start_time = time.time()  # Start timing
    
    sql_query = generate_sql(question)
    #st.text_area("📜 Generated SQL Query:", sql_query, height=100)

    # ✅ Execute SQL Query if it's a SELECT statement
    # if sql_query.strip().lower().startswith("select"):
    #     try:
    #         conn = connect_to_db()
    #         results = execute_query(conn, sql_query)
    #         st.success("✅ Query executed successfully!")
    #         st.write("📊 Query Results:")
    #         st.write(results)
    #     except Exception as e:
    #         st.error(f"⚠️ Error executing query: {e}")
    
    # 🔥 Total Time Taken
    total_time = time.time() - start_time

    st.text_area("📜 Generated SQL Query:", sql_query, height=100)
    st.write(f"⏳ **SQL Generation Time:** {total_time:.2f} seconds")
