import streamlit as st
from utils.Upload import uploader
from utils.Handle import handler
from utils.Analyze import analyzer
from utils.Visualize import visualizer

st.set_page_config(page_title="Data Analysis App", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Upload"

if "df" not in st.session_state:
    st.session_state.df = None

st.title("MINI DATA ANALYZER")

if st.session_state.page == "Upload":

    uploader()

    if st.session_state.df is not None:
        st.dataframe(st.session_state.df, use_container_width=True)

        if st.button("Next"):
            st.session_state.page = "Handle"


elif st.session_state.page == "Handle":

    handler()

elif st.session_state.page == "Analyze":

    analyzer()
    df=st.session_state.df
    col1,col2=st.columns(2)
    with col1:
        if st.button("Back Page"):
            st.session_state.page = "Handle"
    with col2:
        if df.isna().sum().sum()==0 and df.duplicated().sum()==0:
            if st.button("Next Page"):
                st.session_state.page = "Visualize"

elif st.session_state.page=="Visualize":
    visualizer()
    if st.button("Back"):
        st.session_state.page = "Analyze"