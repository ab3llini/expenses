from abc import ABC

import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile

# Abstraction over a bank account statement
# The core logic is to allow to translate an arbitrary streamlit UploadedFile into a DataFrame with a specific schema
# The schema is defined by the following columns:

# "date" - as a datetime object, like 2021-01-01 00:00:00
# "operation" - i.e. "pos" or "atm"
# "euro" - i.e. the euro of money that has been moved
# "kind" - i.e "expense" or "earning"
# "category" - i.e. "food" or "salary"
# "subcategory" - i.e. "groceries" or "rent"
# "description"


# The class is meant to be used as a base class for specific banks
class BankStatement(ABC):
    cols = [
        "date",
        "week",
        "month",
        "operation",
        "euro",
        "kind",
        "category",
        "subcategory",
        "description",
    ]

    def __init__(self, stream: UploadedFile) -> None:
        self.stream = stream

    def df(self) -> pd.DataFrame:
        # Implement the logic to convert the file into a DataFrame
        # The resulting dataframe must have the schema defined above
        raise NotImplementedError


class BancaSella(BankStatement):
    def df(self) -> pd.DataFrame:
        # A banca sella bank statement is a csv file with the following columns: "Codice identificativo",
        # "Data operazione","Data valuta","Descrizione","Divisa","Importo","Categoria","Sottocategoria","Etichette"
        # Let's convert it into the schema defined above
        df = pd.read_csv(self.stream)
        df = df.rename(
            columns={
                "Data operazione": "date",
                "Descrizione": "description",
                "Importo": "euro",
                "Categoria": "category",
                "Sottocategoria": "subcategory",
                "Etichette": "operation",
            }
        )

        # For each column in a set, replace nan with other
        for col in ["category", "subcategory", "operation", "description"]:
            df[col] = df[col].fillna("N.A.")

        df["euro"] = df["euro"].str.replace(".", "")
        df["euro"] = df["euro"].str.replace(",", ".").astype(float)

        df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")

        df = df[~df["date"].isna()]

        df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
        df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)
        df["date"] = df["date"].dt.date

        df["kind"] = df["euro"].apply(lambda x: "expense" if x < 0 else "earning")
        df["euro"] = df["euro"].abs()
        return df[self.cols]


class Revolut(BankStatement):
    def df(self) -> pd.DataFrame:
        # A revolut bank statement is a csv file with the following columns:
        # Type,Product,Started Date,Completed Date,Description,Amount,Fee,Currency,State,Balance
        # Let's convert it into the schema defined above
        df = pd.read_csv(self.stream)
        df = df.rename(
            columns={
                "Started Date": "date",
                "Description": "description",
                "Amount": "euro",
                "Type": "operation",
            }
        )
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d %H:%M:%S")
        df["week"] = df["date"].dt.to_period("W").apply(lambda r: r.start_time)
        df["month"] = df["date"].dt.to_period("M").apply(lambda r: r.start_time)
        df["date"] = df["date"].dt.date
        df["category"] = "Not Available"
        df["subcategory"] = "Not Available"
        df["kind"] = df["euro"].apply(lambda x: "expense" if x < 0 else "earning")
        df["euro"] = df["euro"].abs()
        return df[self.cols]
