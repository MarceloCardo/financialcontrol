import pandas as pd
import sqlite3
from pathlib import Path
from src.utils import ROOT_DOWN_PATH

folder = Path(ROOT_DOWN_PATH)

def load_database():

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
