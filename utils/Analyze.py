import pandas as pd
import streamlit as st

def analyzer():
    st.header("Data Analysis")
    df=st.session_state.df
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Rows",df.shape[0])
    c2.metric("Columns",df.shape[1])
    c3.metric("Missing Values",df.isna().sum().sum())
    c4.metric("Duplicate Rows",df.duplicated().sum())

    numeric_cols = df.select_dtypes(include="number").shape[1]
    object_cols = df.select_dtypes(include="object").shape[1]

    c5,c6=st.columns(2)
    c5.metric("Numeric Columns",numeric_cols)
    c6.metric("Categorical Columns",object_cols)

    if(df.isna().sum().sum()!=0): st.info("Null values are present.Go back and clean the dataset to proceed")
    elif(df.duplicated().sum()!=0): st.info("Duplicate values are present.Go back and clean the dataset to proceed")
    else:
        st.subheader("Column Information")
        col_info = pd.DataFrame({
            "Column Name": df.columns,
            "Data Type": df.dtypes.values
        })
        col_info["Unique Values"]=df.nunique().values
        st.dataframe(col_info, use_container_width=True)


        if numeric_cols>0:
            st.subheader("Data Summary(Numeric):")
            st.write(df.describe())
        else:
            st.info("No Numeric Columns Summary")
        if object_cols>0:
            st.write("Data Summary(Categoric):")
            st.write(df.describe(include="object"))
        else:
            st.info("No Categorical Columns Summary")

        if numeric_cols>1:
            st.subheader("Correlation Matrix")
            corr=df.corr(numeric_only=True)
            st.dataframe(corr,use_container_width=True)