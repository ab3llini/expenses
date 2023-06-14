import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile


def render() -> tuple[UploadedFile | None, int]:
    # File upload
    st.sidebar.subheader("Upload Sella Transactions")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file with bank transactions",
        accept_multiple_files=False,
    )

    st.sidebar.divider()

    st.sidebar.subheader("Settings")

    # Plot Height
    plot_height = st.sidebar.slider(
        "Plot Height", min_value=400, max_value=800, value=500, step=50
    )

    return uploaded_file, plot_height
