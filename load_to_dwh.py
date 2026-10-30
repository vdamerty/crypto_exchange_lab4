
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, URL

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

password = os.getenv("DWH_PASSWORD")

if not password:
    raise ValueError("Пароль DWH_PASSWORD не знайдено у .env")

# Підключення до PostgreSQL лабораторної №4
db_url = URL.create(
    "postgresql+psycopg2",
    username="crypto_admin",
    password=password,
    host="127.0.0.1",
    port=5434,
    database="crypto_lab4"
)

engine = create_engine(db_url)

tables = [
    "traders",
    "currencies",
    "wallets",
    "trades",
    "deposits_withdrawals"
]

def load_data():
    with engine.begin() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS raw")
        )

    for table in tables:
        file_path = BASE_DIR / "data_lake" / f"{table}.parquet"

        df = pd.read_parquet(file_path)

        df.to_sql(
            name=table,
            con=engine,
            schema="raw",
            if_exists="replace",
            index=False,
            chunksize=500
        )

        print(f"Завантажено {table}: {len(df)} записів")

    print("Усі таблиці успішно завантажено у PostgreSQL")

if __name__ == "__main__":
    load_data()
