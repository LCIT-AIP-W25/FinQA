
  CREATE TABLE "ADMIN"."HSBC_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for HSBC_INCOME_QUARTERLY
INSERT INTO "ADMIN"."HSBC_INCOME_QUARTERLY" ("METRICS") VALUES
("Interest Income on Loans"),
("Interest Paid on Deposits"),
("Net Interest Income"),
("Net Interest Income Growth YoY"),
("Income From Trading Activities"),
("Gain Loss on Sale of Assets"),
("Gain Loss on Sale of Investments"),
("Other Non Interest Income"),
("Total Non Interest Income"),
("Non Interest Income Growth YoY"),
("Revenues Before Loan Losses"),
("Provision for Loan Losses"),
("Revenue"),
("Revenue Growth YoY"),
("Salaries and Employee Benefits"),
("Occupancy Expenses"),
("Amortization of Goodwill and Intangibles"),
("Selling General and Administrative"),
("Other Non Interest Expense"),
("Total Non Interest Expense"),
("EBT Excluding Unusual Items"),
("Asset Writedown"),
("Legal Settlements"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Minority Interest in Earnings"),
("Net Income"),
("Preferred Dividends and Other Adjustments"),
("Net Income to Common"),
("Net Income Growth"),
("Basic Shares Outstanding"),
("Diluted Shares Outstanding"),
("Shares Change YoY"),
("EPS Basic"),
("EPS Diluted"),
("EPS Growth"),
("Dividend Per Share"),
("Dividend Growth"),
("Effective Tax Rate");
   (	"METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP", 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126), 
	"Q3_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 


  CREATE TABLE "ADMIN"."HSBC_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for HSBC_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."HSBC_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Investment Securities"),
("Trading Asset Securities"),
("Total Investments"),
("Gross Loans"),
("Allowance for Loan Losses"),
("Other Adjustments to Gross Loans"),
("Net Loans"),
("Property Plant and Equipment"),
("Goodwill"),
("Other Intangible Assets"),
("Other Receivables"),
("Restricted Cash"),
("Other Current Assets"),
("Long Term Deferred Tax Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accrued Expenses"),
("Interest Bearing Deposits"),
("Total Deposits"),
("Short Term Borrowings"),
("Current Portion of Long Term Debt"),
("Current Income Taxes Payable"),
("Other Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Pension and Post Retirement Benefits"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Growth"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share");
   (	"METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP", 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126), 
	"Q3_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 


  CREATE TABLE "ADMIN"."HSBC_CASH_FLOW_QUARTERLY" 
   (	"METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP", 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126), 
	"Q3_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION DEFERRED 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  TABLESPACE "DATA" 


  CREATE TABLE "ADMIN"."HSBC_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for HSBC_RATIO_QUARTERLY
INSERT INTO "ADMIN"."HSBC_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Last Close Price"),
("PE Ratio"),
("PS Ratio"),
("PB Ratio"),
("Debt with Equity Ratio"),
("Return on Equity ROE"),
("Return on Assets ROA"),
("Earnings Yield"),
("Dividend Yield"),
("Buyback Yield with Dilution"),
("Total Shareholder Return");
   (	"METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP", 
	"CURRENT_2025" FLOAT(126), 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126), 
	"Q3_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 

