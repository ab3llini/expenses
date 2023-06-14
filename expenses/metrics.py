import pandas as pd
import streamlit as st
from models import CashFlow


@st.cache_data
def total(df: pd.DataFrame, flow: CashFlow) -> int:
    return int(df[flow].sum())
