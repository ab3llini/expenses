from datetime import date

import pandas as pd
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from dateutil.relativedelta import relativedelta
from expenses.models import CashFlow, CategoryLevel



@st.cache_data
def total(df: pd.DataFrame, flow: CashFlow) -> int:
    return int(df[flow.value].sum())