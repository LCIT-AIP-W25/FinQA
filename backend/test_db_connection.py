from sqlalchemy import create_engine, text

DATABASE_URI = "postgresql+psycopg2://postgres:mypostgres@localhost:5432/finqa"

engine = create_engine(DATABASE_URI)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Connection successful:", result.fetchone())
except Exception as e:
    print("Connection error:", e)



git remote add origin https://github.com/MeghanaSangawar/LCIT-AIP-W25/FinQA.git

