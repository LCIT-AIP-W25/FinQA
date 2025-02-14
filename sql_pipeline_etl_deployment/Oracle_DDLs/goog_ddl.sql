
  CREATE TABLE "ADMIN"."GOOG_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for GOOG_INCOME_QUARTERLY
INSERT INTO "ADMIN"."GOOG_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Research and Development"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Gain Loss on Sale of Investments"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Net Income"),
("Net Income to Common"),
("Net Income Growth"),
("Shares Outstanding Basic"),
("Shares Outstanding Diluted"),
("Shares Change YoY"),
("EPS Basic"),
("EPS Diluted"),
("EPS Growth"),
("Free Cash Flow"),
("Free Cash Flow Per Share"),
("Dividend Per Share"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
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


  CREATE TABLE "ADMIN"."GOOG_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for GOOG_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."GOOG_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Deferred Tax Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Short Term Debt"),
("Current Portion of Long Term Debt"),
("Current Portion of Leases"),
("Current Income Taxes Payable"),
("Current Unearned Revenue"),
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Unearned Revenue"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Retained Earnings"),
("Comprehensive Income and Other"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Growth"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Machinery"),
("Construction In Progress"),
("Leasehold Improvements"),
("Order Backlog");
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


  CREATE TABLE "ADMIN"."GOOG_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for GOOG_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."GOOG_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Asset Writedown and Restructuring Costs"),
("Loss Gain From Sale of Investments"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Accounts Payable"),
("Change in Unearned Revenue"),
("Change in Income Taxes"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Cash Acquisitions"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Repurchase of Common Stock"),
("Common Dividends Paid"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Income Tax Paid"),
("Levered Free Cash Flow"),
("Unlevered Free Cash Flow"),
("Change in Net Working Capital");
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


  CREATE TABLE "ADMIN"."GOOG_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for GOOG_RATIO_QUARTERLY
INSERT INTO "ADMIN"."GOOG_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("EV with Sales Ratio"),
("EV with EBITDA Ratio"),
("EV with EBIT Ratio"),
("EV with FCF Ratio"),
("Debt with Equity Ratio"),
("Debt with EBITDA Ratio"),
("Debt with FCF Ratio"),
("Asset Turnover"),
("Inventory Turnover"),
("Quick Ratio"),
("Current Ratio"),
("Return on Equity ROE"),
("Return on Assets ROA"),
("Return on Capital ROIC"),
("Earnings Yield"),
("FCF Yield"),
("Dividend Yield"),
("Payout Ratio"),
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

