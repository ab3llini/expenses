import pandas as pd
import streamlit as st


@st.cache_data
def total(df: pd.DataFrame, kind: str) -> int:
    return int(df[df.kind == kind]["euro"].sum())
