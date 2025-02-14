-- DDL for META_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."META_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for META_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."META_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Receivables"),
("Prepaid Expenses"),
("Restricted Cash"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Current Portion of Leases"),
("Current Income Taxes Payable"),
("Current Unearned Revenue"),
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Unearned Revenue"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Additional Paid In Capital"),
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
("Buildings"),
("Machinery"),
("Construction In Progress"),
("Leasehold Improvements");
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

-- DDL for META_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."META_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for META_INCOME_QUARTERLY
INSERT INTO "ADMIN"."META_INCOME_QUARTERLY" ("METRICS") VALUES
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
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Gain Loss on Sale of Investments"),
("Pretax Income"),
("Income Tax Expense"),
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

-- DDL for META_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."META_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for META_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."META_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Asset Writedown and Restructuring Costs"),
("Loss Gain From Sale of Investments"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Accounts Payable"),
("Change in Unearned Revenue"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Cash Acquisitions"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
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
("Cash Interest Paid"),
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

-- DDL for META_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."META_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for META_RATIO_QUARTERLY
INSERT INTO "ADMIN"."META_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
("EV with Sales Ratio"),
("EV with EBITDA Ratio"),
("EV with EBIT Ratio"),
("EV with FCF Ratio"),
("Debt with Equity Ratio"),
("Debt with EBITDA Ratio"),
("Debt with FCF Ratio"),
("Asset Turnover"),
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

-- DDL for SHEL_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."SHEL_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for SHEL_INCOME_QUARTERLY
INSERT INTO "ADMIN"."SHEL_INCOME_QUARTERLY" ("METRICS") VALUES
("Operating Revenue"),
("Other Revenue"),
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Research and Development"),
("Other Operating Expenses"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Impairment of Goodwill"),
("Gain Loss on Sale of Assets"),
("Asset Writedown"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Minority Interest in Earnings"),
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
("Dividend Growth"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Revenue as Reported");
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

-- DDL for SHEL_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."SHEL_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for SHEL_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."SHEL_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Accounts Receivable"),
("Long Term Deferred Tax Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Short Term Debt"),
("Current Portion of Long Term Debt"),
("Current Portion of Leases"),
("Current Income Taxes Payable"),
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
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

-- DDL for SHEL_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."SHEL_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for SHEL_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."SHEL_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Loss Gain From Sale of Assets"),
("Asset Writedown and Restructuring Costs"),
("Loss Gain on Equity Investments"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Investment in Securities"),
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
("Common Dividends Paid"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Miscellaneous Cash Flow Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for SHEL_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."SHEL_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for SHEL_RATIO_QUARTERLY
INSERT INTO "ADMIN"."SHEL_RATIO_QUARTERLY" ("METRICS") VALUES
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

-- DDL for MCD_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."MCD_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for MCD_INCOME_QUARTERLY
INSERT INTO "ADMIN"."MCD_INCOME_QUARTERLY" ("METRICS") VALUES
("Operating Revenue"),
("Other Revenue"),
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Other Operating Expenses"),
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
("Gain Loss on Sale of Assets"),
("Asset Writedown"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
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
("Dividend Growth"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Revenue as Reported");
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

-- DDL for MCD_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."MCD_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for MCD_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."MCD_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Trading Asset Securities"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
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
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Unearned Revenue"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Buildings"),
("Machinery");
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

-- DDL for MCD_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."MCD_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for MCD_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."MCD_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Loss Gain From Sale of Assets"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Income Taxes"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Cash Acquisitions"),
("Divestitures"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
("Repurchase of Common Stock"),
("Common Dividends Paid"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Miscellaneous Cash Flow Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for MCD_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."MCD_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for MCD_RATIO_QUARTERLY
INSERT INTO "ADMIN"."MCD_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for KO_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."KO_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for KO_INCOME_QUARTERLY
INSERT INTO "ADMIN"."KO_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Other Operating Expenses"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Impairment of Goodwill"),
("Gain Loss on Sale of Investments"),
("Gain Loss on Sale of Assets"),
("Asset Writedown"),
("Legal Settlements"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Minority Interest in Earnings"),
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
("Dividend Growth"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Advertising Expenses");
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

-- DDL for KO_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."KO_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for KO_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."KO_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Trading Asset Securities"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Restricted Cash"),
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
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Buildings"),
("Machinery");
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

-- DDL for KO_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."KO_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for KO_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."KO_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Loss Gain From Sale of Assets"),
("Asset Writedown and Restructuring Costs"),
("Loss Gain on Equity Investments"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Income Taxes"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Cash Acquisitions"),
("Divestitures"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
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
("Cash Interest Paid"),
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

-- DDL for KO_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."KO_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for KO_RATIO_QUARTERLY
INSERT INTO "ADMIN"."KO_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for GOOG_INCOME_QUARTERLY

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

-- DDL for GOOG_BALANCE_SHEET_QUARTERLY

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

-- DDL for GOOG_CASH_FLOW_QUARTERLY

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

-- DDL for GOOG_RATIO_QUARTERLY

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

-- DDL for VZ_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."VZ_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for VZ_INCOME_QUARTERLY
INSERT INTO "ADMIN"."VZ_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Impairment of Goodwill"),
("Gain Loss on Sale of Assets"),
("Legal Settlements"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Minority Interest in Earnings"),
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
("Dividend Growth"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Revenue as Reported");
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

-- DDL for VZ_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."VZ_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for VZ_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."VZ_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Trading Asset Securities"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Restricted Cash"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Accounts Receivable"),
("Long Term Deferred Charges"),
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
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Buildings"),
("Machinery"),
("Construction In Progress"),
("Leasehold Improvements");
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

-- DDL for VZ_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."VZ_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for VZ_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."VZ_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Asset Writedown and Restructuring Costs"),
("Loss Gain on Equity Investments"),
("Provision and Write off of Bad Debts"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Cash Acquisitions"),
("Divestitures"),
("Sale Purchase of Intangibles"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Common Dividends Paid"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
("Cash Income Tax Paid"),
("Levered Free Cash Flow"),
("Unlevered Free Cash Flow"),
("Change in Net Working Capital");
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

-- DDL for VZ_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."VZ_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for VZ_RATIO_QUARTERLY
INSERT INTO "ADMIN"."VZ_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for JPM_INCOME_QUARTERLY

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

-- DDL for JPM_BALANCE_SHEET_QUARTERLY

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

-- DDL for JPM_CASH_FLOW_QUARTERLY

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

-- DDL for JPM_RATIO_QUARTERLY

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

-- DDL for AMZN_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."AMZN_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for AMZN_INCOME_QUARTERLY
INSERT INTO "ADMIN"."AMZN_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Research and Development"),
("Other Operating Expenses"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Gain Loss on Sale of Investments"),
("Asset Writedown"),
("Pretax Income"),
("Income Tax Expense"),
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
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Revenue as Reported");
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

-- DDL for AMZN_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."AMZN_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for AMZN_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."AMZN_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Restricted Cash"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Short Term Debt"),
("Current Portion of Long Term Debt"),
("Current Portion of Leases"),
("Current Unearned Revenue"),
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Unearned Revenue"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Machinery"),
("Construction In Progress");
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

-- DDL for AMZN_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."AMZN_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for AMZN_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."AMZN_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Unearned Revenue"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Cash Acquisitions"),
("Investment in Securities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Repurchase of Common Stock"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for AMZN_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."AMZN_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for AMZN_RATIO_QUARTERLY
INSERT INTO "ADMIN"."AMZN_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for TSLA_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."TSLA_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for TSLA_INCOME_QUARTERLY
INSERT INTO "ADMIN"."TSLA_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Research and Development"),
("Other Operating Expenses"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Legal Settlements"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Minority Interest in Earnings"),
("Net Income"),
("Preferred Dividends and Other Adjustments"),
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
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Revenue as Reported");
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

-- DDL for TSLA_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."TSLA_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for TSLA_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."TSLA_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Restricted Cash"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Accounts Receivable"),
("Long Term Deferred Tax Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
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
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Machinery"),
("Construction In Progress"),
("Leasehold Improvements");
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

-- DDL for TSLA_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."TSLA_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for TSLA_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."TSLA_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Other Amortization"),
("Loss Gain From Sale of Assets"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Unearned Revenue"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Cash Acquisitions"),
("Sale Purchase of Intangibles"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for TSLA_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."TSLA_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for TSLA_RATIO_QUARTERLY
INSERT INTO "ADMIN"."TSLA_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for NFLX_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."NFLX_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for NFLX_INCOME_QUARTERLY
INSERT INTO "ADMIN"."NFLX_INCOME_QUARTERLY" ("METRICS") VALUES
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
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("Pretax Income"),
("Income Tax Expense"),
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

-- DDL for NFLX_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."NFLX_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for NFLX_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."NFLX_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Prepaid Expenses"),
("Restricted Cash"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Other Intangible Assets"),
("Long Term Deferred Tax Assets"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Short Term Debt"),
("Current Portion of Long Term Debt"),
("Current Portion of Leases"),
("Current Unearned Revenue"),
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Buildings"),
("Machinery"),
("Construction In Progress"),
("Leasehold Improvements");
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

-- DDL for NFLX_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."NFLX_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for NFLX_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."NFLX_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Other Amortization"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Payable"),
("Change in Unearned Revenue"),
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
("Issuance of Common Stock"),
("Repurchase of Common Stock"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
("Cash Income Tax Paid"),
("Levered Free Cash Flow"),
("Unlevered Free Cash Flow"),
("Change in Net Working Capital");
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

-- DDL for NFLX_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."NFLX_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for NFLX_RATIO_QUARTERLY
INSERT INTO "ADMIN"."NFLX_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
("EV with Sales Ratio"),
("EV with EBITDA Ratio"),
("EV with EBIT Ratio"),
("EV with FCF Ratio"),
("Debt with Equity Ratio"),
("Debt with EBITDA Ratio"),
("Debt with FCF Ratio"),
("Asset Turnover"),
("Quick Ratio"),
("Current Ratio"),
("Return on Equity ROE"),
("Return on Assets ROA"),
("Return on Capital ROIC"),
("Earnings Yield"),
("FCF Yield"),
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

-- DDL for SPGI_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."SPGI_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for SPGI_INCOME_QUARTERLY
INSERT INTO "ADMIN"."SPGI_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Gain Loss on Sale of Investments"),
("Gain Loss on Sale of Assets"),
("Asset Writedown"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Net Income to Company"),
("Minority Interest in Earnings"),
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
("Dividend Growth"),
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

-- DDL for SPGI_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."SPGI_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for SPGI_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."SPGI_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Trading Asset Securities"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Receivables"),
("Prepaid Expenses"),
("Restricted Cash"),
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
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Buildings"),
("Machinery");
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

-- DDL for SPGI_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."SPGI_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for SPGI_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."SPGI_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Loss Gain From Sale of Assets"),
("Asset Writedown and Restructuring Costs"),
("Stock Based Compensation"),
("Provision and Write off of Bad Debts"),
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
("Divestitures"),
("Investment in Securities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
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
("Cash Interest Paid"),
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

-- DDL for SPGI_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."SPGI_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for SPGI_RATIO_QUARTERLY
INSERT INTO "ADMIN"."SPGI_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
("EV with Sales Ratio"),
("EV with EBITDA Ratio"),
("EV with EBIT Ratio"),
("EV with FCF Ratio"),
("Debt with Equity Ratio"),
("Debt with EBITDA Ratio"),
("Debt with FCF Ratio"),
("Asset Turnover"),
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

-- DDL for HSBC_INCOME_QUARTERLY

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

-- DDL for HSBC_BALANCE_SHEET_QUARTERLY

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

-- DDL for HSBC_CASH_FLOW_QUARTERLY

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

-- DDL for HSBC_RATIO_QUARTERLY

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

-- DDL for MA_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."MA_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for MA_INCOME_QUARTERLY
INSERT INTO "ADMIN"."MA_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Gross Profit"),
("Selling General and Admin"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Gain Loss on Sale of Investments"),
("Legal Settlements"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
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
("Dividend Growth"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Advertising Expenses");
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

-- DDL for MA_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."MA_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for MA_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."MA_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Receivables"),
("Restricted Cash"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Deferred Tax Assets"),
("Long Term Deferred Charges"),
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
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Buildings"),
("Machinery"),
("Leasehold Improvements");
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

-- DDL for MA_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."MA_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for MA_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."MA_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Other Amortization"),
("Loss Gain From Sale of Investments"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Accounts Payable"),
("Change in Income Taxes"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Cash Acquisitions"),
("Sale Purchase of Intangibles"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
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
("Cash Interest Paid"),
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

-- DDL for MA_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."MA_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for MA_RATIO_QUARTERLY
INSERT INTO "ADMIN"."MA_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
("EV with Sales Ratio"),
("EV with EBITDA Ratio"),
("EV with EBIT Ratio"),
("EV with FCF Ratio"),
("Debt with Equity Ratio"),
("Debt with EBITDA Ratio"),
("Debt with FCF Ratio"),
("Asset Turnover"),
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

-- DDL for AMD_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."AMD_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for AMD_INCOME_QUARTERLY
INSERT INTO "ADMIN"."AMD_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Research and Development"),
("Other Operating Expenses"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Earnings From Equity Investments"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Gain Loss on Sale of Investments"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
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

-- DDL for AMD_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for AMD_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."AMD_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Restricted Cash"),
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
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
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
("Buildings"),
("Machinery"),
("Construction In Progress"),
("Leasehold Improvements");
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

-- DDL for AMD_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."AMD_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for AMD_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."AMD_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Other Amortization"),
("Loss Gain From Sale of Assets"),
("Loss Gain From Sale of Investments"),
("Loss Gain on Equity Investments"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Cash Acquisitions"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Total Debt Issued"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
("Repurchase of Common Stock"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for AMD_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."AMD_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for AMD_RATIO_QUARTERLY
INSERT INTO "ADMIN"."AMD_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with TBV Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for PEP_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."PEP_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for PEP_INCOME_QUARTERLY
INSERT INTO "ADMIN"."PEP_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Research and Development"),
("Other Operating Expenses"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Interest and Investment Income"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Gain Loss on Sale of Investments"),
("Gain Loss on Sale of Assets"),
("Asset Writedown"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Minority Interest in Earnings"),
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
("Dividend Growth"),
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

-- DDL for PEP_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."PEP_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for PEP_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."PEP_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Deferred Tax Assets"),
("Long Term Deferred Charges"),
("Other Long Term Assets"),
("Total Assets"),
("Accounts Payable"),
("Accrued Expenses"),
("Short Term Debt"),
("Current Portion of Long Term Debt"),
("Current Portion of Leases"),
("Other Current Liabilities"),
("Total Current Liabilities"),
("Long Term Debt"),
("Long Term Leases"),
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Buildings"),
("Machinery"),
("Construction In Progress");
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

-- DDL for PEP_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."PEP_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for PEP_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."PEP_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Other Amortization"),
("Loss Gain From Sale of Assets"),
("Asset Writedown and Restructuring Costs"),
("Stock Based Compensation"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Income Taxes"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Cash Acquisitions"),
("Divestitures"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
("Repurchase of Common Stock"),
("Common Dividends Paid"),
("Dividends Paid"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Foreign Exchange Rate Adjustments"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for PEP_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."PEP_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for PEP_RATIO_QUARTERLY
INSERT INTO "ADMIN"."PEP_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

-- DDL for T_INCOME_QUARTERLY

  CREATE TABLE "ADMIN"."T_INCOME_QUARTERLY" 

-- Insert values into the METRICS column for T_INCOME_QUARTERLY
INSERT INTO "ADMIN"."T_INCOME_QUARTERLY" ("METRICS") VALUES
("Revenue"),
("Revenue Growth YoY"),
("Cost of Revenue"),
("Gross Profit"),
("Selling General and Admin"),
("Operating Expenses"),
("Operating Income"),
("Interest Expense"),
("Earnings From Equity Investments"),
("Currency Exchange Gain Loss"),
("Other Non Operating Income Expenses"),
("EBT Excluding Unusual Items"),
("Merger and Restructuring Charges"),
("Impairment of Goodwill"),
("Gain Loss on Sale of Investments"),
("Gain Loss on Sale of Assets"),
("Asset Writedown"),
("Other Unusual Items"),
("Pretax Income"),
("Income Tax Expense"),
("Earnings From Continuing Operations"),
("Earnings From Discontinued Operations"),
("Net Income to Company"),
("Minority Interest in Earnings"),
("Net Income"),
("Preferred Dividends and Other Adjustments"),
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
("Dividend Growth"),
("Gross Margin"),
("Operating Margin"),
("Profit Margin"),
("Free Cash Flow Margin"),
("EBITDA"),
("EBITDA Margin"),
("D and A For EBITDA"),
("EBIT"),
("EBIT Margin"),
("Effective Tax Rate"),
("Revenue as Reported");
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

-- DDL for T_BALANCE_SHEET_QUARTERLY

  CREATE TABLE "ADMIN"."T_BALANCE_SHEET_QUARTERLY" 

-- Insert values into the METRICS column for T_BALANCE_SHEET_QUARTERLY
INSERT INTO "ADMIN"."T_BALANCE_SHEET_QUARTERLY" ("METRICS") VALUES
("Cash and Equivalents"),
("Short Term Investments"),
("Trading Asset Securities"),
("Cash and Short Term Investments"),
("Cash Growth"),
("Accounts Receivable"),
("Other Receivables"),
("Receivables"),
("Inventory"),
("Prepaid Expenses"),
("Restricted Cash"),
("Other Current Assets"),
("Total Current Assets"),
("Property Plant and Equipment"),
("Long Term Investments"),
("Goodwill"),
("Other Intangible Assets"),
("Long Term Deferred Charges"),
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
("Long Term Deferred Tax Liabilities"),
("Other Long Term Liabilities"),
("Total Liabilities"),
("Common Stock"),
("Additional Paid In Capital"),
("Retained Earnings"),
("Treasury Stock"),
("Comprehensive Income and Other"),
("Total Common Equity"),
("Minority Interest"),
("Shareholders Equity"),
("Total Liabilities and Equity"),
("Total Debt"),
("Net Cash Debt"),
("Net Cash Per Share"),
("Filing Date Shares Outstanding"),
("Total Common Shares Outstanding"),
("Working Capital"),
("Book Value Per Share"),
("Tangible Book Value"),
("Tangible Book Value Per Share"),
("Land"),
("Buildings"),
("Machinery"),
("Construction In Progress");
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

-- DDL for T_CASH_FLOW_QUARTERLY

  CREATE TABLE "ADMIN"."T_CASH_FLOW_QUARTERLY" 

-- Insert values into the METRICS column for T_CASH_FLOW_QUARTERLY
INSERT INTO "ADMIN"."T_CASH_FLOW_QUARTERLY" ("METRICS") VALUES
("Net Income"),
("Depreciation and Amortization"),
("Other Amortization"),
("Asset Writedown and Restructuring Costs"),
("Loss Gain From Sale of Investments"),
("Loss Gain on Equity Investments"),
("Provision and Write off of Bad Debts"),
("Other Operating Activities"),
("Change in Accounts Receivable"),
("Change in Inventory"),
("Change in Accounts Payable"),
("Change in Other Net Operating Assets"),
("Operating Cash Flow"),
("Operating Cash Flow Growth"),
("Capital Expenditures"),
("Sale of Property Plant and Equipment"),
("Cash Acquisitions"),
("Investment in Securities"),
("Other Investing Activities"),
("Investing Cash Flow"),
("Short Term Debt Issued"),
("Long Term Debt Issued"),
("Total Debt Issued"),
("Short Term Debt Repaid"),
("Long Term Debt Repaid"),
("Total Debt Repaid"),
("Net Debt Issued Repaid"),
("Issuance of Common Stock"),
("Repurchase of Common Stock"),
("Common Dividends Paid"),
("Dividends Paid"),
("Other Financing Activities"),
("Financing Cash Flow"),
("Net Cash Flow"),
("Free Cash Flow"),
("Free Cash Flow Growth"),
("Free Cash Flow Margin"),
("Free Cash Flow Per Share"),
("Cash Interest Paid"),
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

-- DDL for T_RATIO_QUARTERLY

  CREATE TABLE "ADMIN"."T_RATIO_QUARTERLY" 

-- Insert values into the METRICS column for T_RATIO_QUARTERLY
INSERT INTO "ADMIN"."T_RATIO_QUARTERLY" ("METRICS") VALUES
("Market Capitalization"),
("Market Cap Growth"),
("Enterprise Value"),
("Last Close Price"),
("PE Ratio"),
("Forward PE"),
("PS Ratio"),
("PB Ratio"),
("P with FCF Ratio"),
("P with OCF Ratio"),
("PEG Ratio"),
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

