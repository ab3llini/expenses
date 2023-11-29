from datetime import date

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


@st.cache_data
def load_df(file: UploadedFile | None) -> pd.DataFrame | None:
    return pd.read_csv(file) if file else None


@st.cache_data
def within_period(df: pd.DataFrame, date_from: date, date_to: date) -> pd.DataFrame:
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
