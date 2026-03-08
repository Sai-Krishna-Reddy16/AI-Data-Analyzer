import streamlit as st
import pandas as pd

def uploader():
    st.header("Data Set Upload")
    file = st.file_uploader("Upload CSV or Excel file:")

    if file is not None:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type")
            return
        st.session_state.df=df
        st.success("File uploaded successfully!")

    # else:
    #     st.warning("Upload a file to analyze")