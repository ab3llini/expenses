from datetime import date

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from dateutil.relativedelta import relativedelta
from expenses.models import CashFlow, CategoryLevel



@st.cache_data
def load_df(file: UploadedFile | None) -> pd.DataFrame:
    return pd.read_csv(file) if file else None


@st.cache_data
def transform(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    out = out[
        [
            "Data operazione",
            "Descrizione",
            "Categoria",
            "Sottocategoria",
            "Etichette",
            "Debito",
            "Credito",
        ]
    ]

    out = out.rename(
        columns={
            "Data operazione": "date",
            "Categoria":CategoryLevel.Large,
            "Descrizione": "description",
            "Sottocategoria": CategoryLevel.Small,
            "Etichette": "operation",
            "Debito": CashFlow.Expense.value,
            "Credito": CashFlow.Earning.value,
        }
    )

    for cash_flow in CashFlow:
        out[cash_flow.value] = out[cash_flow.value].str.replace(".", "")
        out[cash_flow.value] = out[cash_flow.value].str.replace(",", ".").astype(float)

    out.loc[:, CashFlow.Expense.value] *= -1

    out["date"] = pd.to_datetime(out["date"], format="%d/%m/%Y")
    out["week"] = out["date"].dt.to_period("W").apply(lambda r: r.start_time)
    out["month"] = out["date"].dt.to_period("M").apply(lambda r: r.start_time)
    out["date"] = out["date"].dt.date

    return out


@st.cache_data
def normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Remove money from cb - 1k
    out = out[~((out[CashFlow.Earning.value] == 1000) & (out["description"].str.contains("MENSILE")))]
    # Assume rent is 1k less
    out.loc[
        (out[CashFlow.Expense.value] == 1200) & (out["description"].str.contains("AFFITTO")), CashFlow.Expense.value
    ] -= 1000

    return out


@st.cache_data
def focus(df: pd.DataFrame, date_from: date, date_to: date) -> pd.DataFrame:

    # first_day_curr_month = date_from.replace(day=1)
    # first_day_next_month = date_to.replace(day=1) + relativedelta(months=1)

    return df[(df["date"] >= date_from) & (df["date"] <= date_to)]

