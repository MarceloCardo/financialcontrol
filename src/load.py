from ofxparse.ofxparse import Ofx, Account, Transaction
import pandas as pd
from ofxparse import OfxParser
from src.utils import ROOT_DOWN_PATH
from pathlib import Path
import sqlite3
import hashlib
folder = Path(ROOT_DOWN_PATH)

print(ROOT_DOWN_PATH)


def load_database():

    data = []
    for filename in folder.glob("*.ofx"):
        # print(file)
        with open(filename, encoding='utf-8') as fileobj:
            ofx: Ofx = OfxParser.parse(fileobj)
            for acc in ofx.accounts:  # type: ignore
                acc: Account

                if not acc.statement:
                    continue

                for stt in acc.statement.transactions:
                    stt: Transaction

                    data.append({
                        "date": stt.date,
                        "name": stt.memo,
                        "amount": stt.amount
                    })

    df = pd.DataFrame(data)

    df["date"] = pd.to_datetime(df["date"])
    df["month_name"] = df["date"].dt.month_name()
    df["year"] = df["date"].dt.year
    df["month_number"] = df["date"].dt.month
    df["name"] = df["name"].astype(str).str.strip()
    df["amount"] = df["amount"].astype(float)

    df["date"] = df["date"].dt.date

    # create unique hash code
    df["unique_key"] = (
        df["date"].astype(str) +
        "|" +
        df["name"] +
        "|" +
        df["amount"].astype(str)
    ).apply(lambda x: hashlib.sha256(x.encode()).hexdigest())

    df = df.drop_duplicates(subset=["unique_key"])

    db_path = Path("database") / "financial.db"
    parquet_path = Path("database") / "financial.parquet"

    engine = sqlite3.connect(db_path)
    cursor = engine.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS nubankFinance (
                        [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                        [date] DATE,
                        [month_name] TEXT,
                        [month_number] INT,
                        [year] INT,
                        [name] TEXT,
                        [amount] FLOAT,
                        [unique_key] TEXT UNIQUE
                )
                """)


    df_db = pd.read_sql("SELECT [unique_key] from nubankFinance", con=engine)
    
    df = df[~df["unique_key"].isin(df_db["unique_key"])]
    
    if not df.empty:
        try:
            df.to_sql(name='nubankFinance', con=engine,
                  if_exists="append", index=False)
            print('carregado para o banco')
        except NotImplementedError as e:
            raise e

    df.to_parquet(parquet_path, partition_cols=["year", "month_number"])
    print('backup parset criado')


if __name__ == '__main__':
    load_database()
