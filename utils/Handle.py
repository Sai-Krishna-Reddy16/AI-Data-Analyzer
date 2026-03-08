import pandas as pd
import streamlit as st

def handler():
    st.header("Data Cleaning And Handling")

    if "step" not in st.session_state:
        st.session_state.step = 1

    df = st.session_state.df

    if st.session_state.step == 1:

        st.subheader("Step 1: Remove Duplicates")

        dup_count = df.duplicated().sum()
        st.write("Duplicate rows:", dup_count)

        if dup_count > 0:
            if st.button("Remove Duplicates"):
                before = len(df)
                df = df.drop_duplicates()
                st.session_state.df = df
                after = len(df)
                st.success(f"{before - after} rows removed")
        else:
            st.info("No duplicates found")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back Page"):
                st.session_state.page="Upload"
        with col2:
            if st.button("Move to Step2"):
                st.session_state.step = 2


    elif st.session_state.step == 2:

        st.subheader("Step 2: Handle Null Values")

        total_nulls = df.isna().sum().sum()
        st.write(df.isna().sum().reset_index(name="Null Count"))

        if total_nulls == 0:
            st.success("No null values found")
        else:
            choice = st.radio(
                "Choose cleaning method:",
                ["Drop rows with any null",
                 "Replace with 0",
                 "Replace with mean",
                 "Replace with median"],
                index=None
            )

            if st.button("Apply Cleaning"):
                if choice is not None:

                    numeric_cols = df.select_dtypes(include="number").columns
                    object_cols = df.select_dtypes(include="object").columns

                    if choice == "Drop rows with any null":
                        df = df.dropna(subset=numeric_cols)

                    elif choice == "Replace with 0":
                        df[numeric_cols] = df[numeric_cols].fillna(0)
                        df[object_cols] = df[object_cols].fillna("Unknown")

                    elif choice == "Replace with mean":
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        df[object_cols] = df[object_cols].fillna("Unknown")

                    elif choice == "Replace with median":
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
                        df[object_cols] = df[object_cols].fillna("Unknown")

                    st.session_state.df = df
                    st.success("Null values handled successfully")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Step1"):
                st.session_state.step = 1
        with col2:
            if st.button("Move to Step3"):
                st.session_state.step = 3


    elif st.session_state.step == 3:

        st.subheader("Step 3: Rename Column")

        col = st.selectbox("Select column", df.columns)
        new_name = st.text_input("Enter new name")

        if st.button("Rename"):
            if new_name.strip() != "" and new_name not in df.columns:
                df.rename(columns={col: new_name}, inplace=True)
                st.session_state.df = df
                st.success("Column renamed successfully")
            else:
                st.warning("Invalid or duplicate column name")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Step2"):
                st.session_state.step = 2
        with col2:
            if st.button("Next Page"):
                st.session_state.page="Analyze"