import pandas as pd
import hashlib
from ofxparse.ofxparse import Ofx, Account, Transaction, OfxParser
from pathlib import Path
from src.utils import ROOT_DOWN_PATH

folder = Path(ROOT_DOWN_PATH)

def transform(folder):
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

    df_raw_data = df.drop_duplicates(subset=["unique_key"])
    
    return df_raw_data