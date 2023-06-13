from datetime import date
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from datetime import timedelta
from expenses.models import Granularity


def render() -> tuple[UploadedFile | None, date, date, Granularity, int]:
    # Sidebar
    st.sidebar.title("Dashboard Settings")

    # File upload
    st.sidebar.subheader("Upload Bank Transactions")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file with bank transactions",
        accept_multiple_files=False,
    )

    # Date range selector
    st.sidebar.subheader("Rendering Settings")
    date_from = st.sidebar.date_input(
        "Start Date", help="Select the start date for the dashboard", value=date.today() - timedelta(days=365)
    )
    date_to = st.sidebar.date_input(
        "End Date", help="Select the end date for the dashboard", value=date.today()
    )

    # Granularity selector
    granularity = st.sidebar.selectbox(
        "Granularity", [grain.value for grain in Granularity]
    )

    # Plot Height
    plot_height = st.sidebar.slider("Plot Height", min_value=400, max_value=800, value=500, step=50)

    return uploaded_file, date_from, date_to, granularity, plot_height
