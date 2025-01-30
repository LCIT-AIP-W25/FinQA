CREATE TABLE FinancialData (
    Metrics VARCHAR(255) NOT NULL CHECK (
        Metrics IN ('Accounts Receivable', 'Total Assets', 'Cash & Equivalents', 'Short-Term Investments', 'Inventory', 'Total Liabilities')
    ) COMMENT 'Categorical column: Filters specific financial metrics',
   
    Q4_2024 DECIMAL(15,4),
    Q3_2024 DECIMAL(15,4),
    Q2_2024 DECIMAL(15,4),
    Q1_2024 DECIMAL(15,4),
    Q4_2023 DECIMAL(15,4),
    Q3_2023 DECIMAL(15,4),
    Q2_2023 DECIMAL(15,4),
    Q1_2023 DECIMAL(15,4),
    Q4_2022 DECIMAL(15,4),
    Q3_2022 DECIMAL(15,4),
    Q2_2022 DECIMAL(15,4),
    Q1_2022 DECIMAL(15,4),
    Q4_2021 DECIMAL(15,4),
    Q3_2021 DECIMAL(15,4),
    Q2_2021 DECIMAL(15,4),
    Q1_2021 DECIMAL(15,4)
);