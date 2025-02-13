import time
import ollama
import mysql.connector
import streamlit as st
import pandas as pd
from pathlib import Path
import openpyxl

# Configuration
DDL_FILE = "schema.sql"
EXCEL_DIR = "excel_files"
QUESTIONS_FILE = "test_questions.txt"

# ======================== DDL Generation & Execution ========================

def generate_ddl_from_excel(excel_path: Path, output_file: Path):
    """Generate DDL from Excel financial data files"""
    wb = openpyxl.load_workbook(excel_path)
    
    with open(output_file, "a") as f:
        for sheet_name in wb.sheetnames:
            # Read Excel sheet
            df = pd.read_excel(excel_path, sheet_name=sheet_name)
            
            # Get company name from filename (e.g., "META.xlsx" -> "META")
            company = excel_path.stem.split("_")[0]  
            table_name = f"{company}_{sheet_name.lower()}"
            
            # Generate CREATE TABLE statement
            ddl = [f'CREATE TABLE {table_name} (']
            
            # First column is metric (primary key)
            ddl.append(f'    {df.columns[0]} VARCHAR(255) PRIMARY KEY CHECK ({df.columns[0]} IN (')
            ddl.append("        'Cash & Equivalents', 'Short-Term Investments', ...")  # Add all valid values
            
            # Add quarterly columns (assume format: "Q3_2024")
            for col in df.columns[1:]:
                ddl.append(f'    "{col}" DECIMAL(15,4),')
            
            ddl[-1] = ddl[-1].rstrip(',')  # Remove last comma
            ddl.append(');\n')
            
            f.write("\n".join(ddl))

def execute_ddl_from_file(conn, ddl_file: Path):
    """Execute SQL DDL commands from file"""
    with open(ddl_file) as f:
        sql = f.read()
        statements = [s.strip() for s in sql.split(';') if s.strip()]
        
    cursor = conn.cursor()
    for stmt in statements:
        try:
            cursor.execute(stmt)
        except mysql.connector.Error as err:
            print(f"Error executing: {stmt}\n{err}")
    conn.commit()

# ======================== Query Generation & Execution ========================

def generate_sql(question: str, ddl_info: str) -> str:
    """Generate SQL using LLM with proper error handling"""
    try:
        prompt = f"Convert to SQL using this schema:\n{ddl_info}\nQuestion: {question}"
        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
        
        sql = response['message']['content']
        if "```sql" in sql:
            sql = sql.split("```sql")[1].split("```")[0].strip()
        return sql
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None

def test_queries(conn):
    """Execute test questions and verify results"""
    with open(QUESTIONS_FILE) as f:
        questions = [q.strip() for q in f.readlines() if q.strip()]
    
    results = []
    for question in questions:
        start_time = time.time()
        
        try:
            # Get relevant DDL for the question
            ddl_info = get_relevant_ddl(question)  # Implement table selection logic
            sql = generate_sql(question, ddl_info)
            
            # Execute query
            cursor = conn.cursor()
            cursor.execute(sql)
            
            # Record results
            execution_time = time.time() - start_time
            results.append({
                "Question": question,
                "SQL": sql,
                "Status": "Success" if cursor.rowcount > 0 else "No results",
                "Execution Time": f"{execution_time:.2f}s"
            })
            
        except Exception as e:
            results.append({
                "Question": question,
                "SQL": sql,
                "Status": f"Error: {str(e)}",
                "Execution Time": "-"
            })
    
    return pd.DataFrame(results)

# ======================== Streamlit UI ========================

def main():
    st.title("📊 Financial Data SQL Assistant")
    
    # Step 1: Initialize Database
    if st.button("🚀 Initialize Database"):
        with st.spinner("Creating tables..."):
            conn = connect_to_db()
            
            # Process all Excel files
            for excel_file in Path(EXCEL_DIR).glob("*.xlsx"):
                generate_ddl_from_excel(excel_file, DDL_FILE)
            
            # Execute generated DDL
            execute_ddl_from_file(conn, DDL_FILE)
            #st.success(f"Database initialized with {len(list(Path(EXCEL_DIR).glob('*.xlsx'))} companies!")\
            st.success(f"Database initialized with {len(list(Path(EXCEL_DIR).glob('*.xlsx')))} companies!")

    
    # Step 2: Test Queries
    if st.button("🧪 Run Test Suite"):
        with st.spinner("Executing test cases..."):
            conn = connect_to_db()
            results = test_queries(conn)
            st.dataframe(results)
            
            # Show success rate
            success_rate = len(results[results["Status"] == "Success"]) / len(results)
            st.metric("Test Success Rate", f"{success_rate:.0%}")

if __name__ == "__main__":
    main()