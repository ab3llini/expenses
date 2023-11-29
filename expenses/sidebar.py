import pandas as pd
import streamlit as st
from statements import BancaSella, Revolut

supported_statements = {
    f"{statement.__name__}": statement for statement in [Revolut, BancaSella]
}


def render() -> tuple[pd.DataFrame | None, int]:
    df = None

    st.sidebar.subheader("Upload Bank Statement")
    bank_name = st.sidebar.selectbox(
        "Bank Name",
        ["Select.."] + list(supported_statements.keys()),
        help="Select your bank",
    )

    if bank_name != "Select..":
        uploaded_file = st.sidebar.file_uploader(
            "Choose a file",
            type=["csv"],
            help="Upload your bank statement",
            accept_multiple_files=False,
        )

        if uploaded_file is not None and bank_name is not None:
            statement = supported_statements[bank_name](uploaded_file)
            df = statement.df()
            st.sidebar.success(f"File {uploaded_file.name} successfully uploaded!")

    st.sidebar.divider()

    st.sidebar.subheader("Settings")

    # Plot Height
    plot_height = st.sidebar.slider(
        "Plot Height", min_value=400, max_value=800, value=500, step=50
    )

    return df, plot_height
