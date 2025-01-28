import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

# Define headers for the HTTP request for web scraping
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

# Quarter Mapping Based on Month
QUARTER_MAPPING = {
    3: "Jan-Mar Q1",
    6: "Apr-Jun Q2",
    9: "July-Sept Q3",
    12: "Oct-Dec Q4"
}


def get_urls(stock_symbol):
    """
    Generate URLs for different financial statements for a given stock symbol.
    Args:
        stock_symbol (str): The stock symbol for which URLs need to be generated.
    Returns:
        dict: A dictionary containing URLs for income, balance sheet, cash flow, and ratio quarterly statements.
    """
    base_url = f"https://stockanalysis.com/stocks/{stock_symbol}/financials"
    return {
        'income quarterly': f"{base_url}/?p=quarterly",
        'balance sheet quarterly': f"{base_url}/balance-sheet/?p=quarterly",
        'cash flow quarterly': f"{base_url}/cash-flow-statement/?p=quarterly",
        'ratio quarterly': f"{base_url}/ratios/?p=quarterly"
    }


def format_fiscal_quarter(fq, stock_symbol):
    """
    Format the fiscal quarter information extracted from the data.
    Args:
        fq (str): Raw fiscal quarter information from the dataset.
        stock_symbol (str): The stock symbol.
    Returns:
        str: Formatted fiscal quarter, e.g., "GOOG - Q1 2021".
    """
    try:
        date = pd.to_datetime(' '.join(fq.split()[-3:]), errors='coerce')
        if pd.isnull(date):
            return None
        year = date.year
        quarter = QUARTER_MAPPING.get(date.month, 'Current')
        return f"{stock_symbol.upper()} - {quarter} {year}"
    except Exception as error:
        print(f"Error formatting fiscal quarter: {fq}, Error: {error}")
        return None


def process_table(url, sheet_name, cutoff_date, xlwriter, stock_symbol):
    """
    Extract financial table data from a webpage and process it into an Excel sheet.
    Args:
        url (str): Web page URL containing financial data.
        sheet_name (str): Name of the sheet in the Excel file.
        cutoff_date (str): The cutoff date for filtering data.
        xlwriter (ExcelWriter): Pandas Excel writer instance.
        stock_symbol (str): The stock symbol for reference.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        table_html = str(soup.find("table", {"id": "main-table"}))
        
        if not table_html:
            print(f"No table found for {sheet_name}")
            return

        df = pd.read_html(StringIO(table_html))[0]

        # Handle MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[1] if isinstance(col, tuple) and len(col) > 1 else col for col in df.columns]

        # Transpose the DataFrame
        df_transposed = df.set_index(df.columns[0]).T.reset_index()
        df_transposed.rename(columns={"index": "Fiscal Quarter"}, inplace=True)

        # Convert Fiscal Quarter to datetime for filtering
        df_transposed['Actual Year-Month'] = df_transposed['Fiscal Quarter'].apply(
            lambda x: pd.to_datetime(' '.join(x.split()[-3:]), errors='coerce') if isinstance(x, str) else pd.NaT
        )
        df_transposed = df_transposed.dropna(subset=['Actual Year-Month'])
        df_transposed['Actual Year-Month'] = df_transposed['Actual Year-Month'].dt.strftime('%Y-%m')

        # Apply cutoff filtering
        df_transposed = df_transposed[df_transposed['Actual Year-Month'] >= cutoff_date]

        # Format Fiscal Quarter
        df_transposed['Fiscal Quarter'] = df_transposed['Fiscal Quarter'].apply(
            lambda x: format_fiscal_quarter(x, stock_symbol)
        )

        # Drop unnecessary columns
        df_transposed = df_transposed.drop(columns=['Actual Year-Month'])

        #Save the final file into excel format
        df_transposed.to_excel(xlwriter, sheet_name=sheet_name, index=False)

    except Exception as error:
        print(f"Error processing {sheet_name}: {error}")


def main():
    """
    Main function to extract financial data for multiple companies and save each in a separate Excel file.
    """
    stock_symbols = ['goog', 'amzn', 'meta', 'tsla', 'jpm', 'ma', 'nflx', 'ko', 'mcd', 'pep', 'shel', 'amd', 'hsbc', 't', 'vz', 'spgi']  # List of stock symbols to process
    cutoff_date = "2021-03"  # Cutoff year-month

    for stock_symbol in stock_symbols:
        output_file = f'financial_statements_{stock_symbol}.xlsx'
        xlwriter = pd.ExcelWriter(output_file, engine='xlsxwriter')

        urls = get_urls(stock_symbol)
        for sheet_name, url in urls.items():
            process_table(url, sheet_name, cutoff_date, xlwriter, stock_symbol)

        xlwriter.close()
        print(f"Financial statements saved: {output_file}")


if __name__ == "__main__":
    main()
