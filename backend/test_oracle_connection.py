import oracledb

connection = oracledb.connect(
    user="ADMIN",
    password="Finanswer@2025",
    dsn="finanswer1_high",
    config_dir=r"C:\Oracle\Wallets\Wallet_FinAnswer1",
    wallet_location=r"C:\Oracle\Wallets\Wallet_FinAnswer1"
    
)

cursor = connection.cursor()
cursor.execute("SELECT DISTINCT COMPANY_NAME FROM COMPANY_MAPPING")
rows = cursor.fetchall()

print("✅ Company Names:", rows)

cursor.close()
connection.close()
