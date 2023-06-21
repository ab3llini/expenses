from datetime import date

import pandas as pd
import streamlit as st
from models import CashFlow, CategoryLevel
from streamlit.runtime.uploaded_file_manager import UploadedFile


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
            "Categoria": CategoryLevel.Large,
            "Descrizione": "description",
            "Sottocategoria": CategoryLevel.Small,
            "Etichette": "operation",
            "Debito": CashFlow.Expense,
            "Credito": CashFlow.Earning,
        }
    )

    # For each column in a set, replace nan with other
    for col in [CategoryLevel.Large, CategoryLevel.Small, "operation", "description"]:
        out[col] = out[col].fillna("N.A.")

    for cash_flow in CashFlow:
        out[cash_flow] = out[cash_flow].str.replace(".", "")
        out[cash_flow] = out[cash_flow].str.replace(",", ".").astype(float)

    out.loc[:, CashFlow.Expense] *= -1

    out["date"] = pd.to_datetime(out["date"], format="%d/%m/%Y")
    out["week"] = out["date"].dt.to_period("W").apply(lambda r: r.start_time)
    out["month"] = out["date"].dt.to_period("M").apply(lambda r: r.start_time)
    out["date"] = out["date"].dt.date

    out = out[~out["date"].isna()]

    return out


@st.cache_data
def normalize(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # Remove money from cb - 1k
    out = out[
        ~(
            (out[CashFlow.Earning] == 1000)
            & (out["description"].str.contains("MENSILE"))
        )
    ]
    # Assume rent is 1k less
    out.loc[
        (out[CashFlow.Expense] == 1200) & (out["description"].str.contains("AFFITTO")),
        CashFlow.Expense,
    ] -= 1000

    return out


@st.cache_data
def within_period(df: pd.DataFrame, date_from: date, date_to: date) -> pd.DataFrame:
    # first_day_curr_month = date_from.replace(day=1)
    # first_day_next_month = date_to.replace(day=1) + relativedelta(months=1)

    return df[(df["date"] >= date_from) & (df["date"] <= date_to)]


@st.cache_data
def filter_choices(df: pd.DataFrame, col: str, choices: list[str]) -> pd.DataFrame:
    return df[df[col].isin(choices)]


@st.cache_data
def earliest_date(df: pd.DataFrame) -> date:
    return df["date"].min()


@st.cache_data
def latest_date(df: pd.DataFrame) -> date:
    return df["date"].max()


@st.cache_data
def choices(df: pd.DataFrame, col: str) -> list[str]:
    return df[col].unique().tolist()
