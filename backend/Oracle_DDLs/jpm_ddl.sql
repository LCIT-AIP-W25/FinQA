
  CREATE TABLE "ADMIN"."JPM_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for JPM_INCOME_QUARTERLY
INSERT INTO "ADMIN"."JPM_INCOME_QUARTERLY" ("METRICS") VALUES
("Interest Income on Loans"),
("Interest Paid on Deposits"),
("Net Interest Income"),
("Net Interest Income Growth YoY"),
("Trust Income"),
("Mortgage Banking Activities"),
("Income From Trading Activities"),
("Gain Loss on Sale of Assets"),
("Gain Loss on Sale of Investments"),
("Gain Loss on Sale of Equity Investments"),
("Other Non Interest Income"),
("Total Non Interest Income"),
("Non Interest Income Growth YoY"),
("Revenues Before Loan Losses"),
("Provision for Loan Losses"),
("Revenue"),
("Revenue Growth YoY"),
("Salaries and Employee Benefits"),
("Occupancy Expenses"),
("Selling General and Administrative"),
("Other Non Interest Expense"),
("Total Non Interest Expense"),
("EBT Excluding Unusual Items"),
("Legal Settlements"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
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
	"Q4_2024" FLOAT(126), 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 


  CREATE TABLE "ADMIN"."JPM_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for JPM_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."JPM_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Investment Securities"),
("Trading Asset Securities"),
("Mortgage Backed Securities"),
("Total Investments"),
("Gross Loans"),
("Allowance for Loan Losses"),
("Net Loans"),
("Property Plant and Equipment"),
("Goodwill"),
("Other Intangible Assets"),
("Loans Held for Sale"),
("Accrued Interest Receivable"),
("Restricted Cash"),
("Other Current Assets"),
("Other Real Estate Owned and Foreclosed"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Interest Bearing Deposits"),
("Institutional Deposits"),
("Non Interest Bearing Deposits"),
("Total Deposits"),
("Short Term Borrowings"),
("Current Portion of Long Term Debt"),
("Current Portion of Leases"),
("Other Current Liabilities"),
("Long Term Debt"),
("Federal Home Loan Bank Debt Long Term"),
("Long Term Leases"),
("Trust Preferred Securities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Preferred Stock Redeemable"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
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
	"Q4_2024" FLOAT(126), 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 


  CREATE TABLE "ADMIN"."JPM_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for JPM_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."JPM_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Provision for Credit Losses"),
("Net Decrease Increase in Loans Originated with Sold Operating"),
("Change in Trading Asset Securities"),
("Accrued Interest Receivable"),
("Change in Accounts Payable"),
("Change in Other Net Operating Assets"),
("Other Operating Activities"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Cash Acquisitions"),
("Investment in Securities"),
("Net Decrease Increase in Loans Originated with Sold Investing"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Repurchase of Common Stock"),
("Preferred Stock Issued"),
("Preferred Share Repurchases"),
("Total Dividends Paid"),
("Net Increase Decrease in Deposit Accounts"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
("Cash Income Tax Paid");
   (	"METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP", 
	"Q4_2024" FLOAT(126), 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 


  CREATE TABLE "ADMIN"."JPM_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for JPM_RATIO_QUARTERLY
INSERT INTO "ADMIN"."JPM_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Last Close Price"),
("PE Ratio"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("Debt with Equity Ratio"),
("Debt with FCF Ratio"),
("Return on Equity ROE"),
("Return on Assets ROA"),
("Earnings Yield"),
("FCF Yield"),
("Dividend Yield"),
("Payout Ratio"),
("Buyback Yield with Dilution"),
("Total Shareholder Return");
   (	"METRICS" VARCHAR2(255) COLLATE "USING_NLS_COMP", 
	"CURRENT_2025" FLOAT(126), 
	"Q4_2024" FLOAT(126), 
	"Q3_2024" FLOAT(126), 
	"Q2_2024" FLOAT(126), 
	"Q1_2024" FLOAT(126), 
	"Q4_2023" FLOAT(126), 
	"Q3_2023" FLOAT(126), 
	"Q2_2023" FLOAT(126), 
	"Q1_2023" FLOAT(126), 
	"Q4_2022" FLOAT(126)
   )  DEFAULT COLLATION "USING_NLS_COMP" SEGMENT CREATION IMMEDIATE 
  PCTFREE 10 PCTUSED 40 INITRANS 10 MAXTRANS 255 
 COLUMN STORE COMPRESS FOR QUERY HIGH ROW LEVEL LOCKING LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1
  BUFFER_POOL DEFAULT FLASH_CACHE DEFAULT CELL_FLASH_CACHE DEFAULT)
  TABLESPACE "DATA" 

