import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
def show_fig(fig):
    st.plotly_chart(fig)

    st.download_button("Download Chart",fig.to_image(format="png"),"chart.png")

def visualizer():
    st.title("Visualization")
    df=st.session_state.df
    title=st.text_input("Chart Title(optional)",placeholder="Enter chart title")
    chart=st.selectbox("Select chart type",['Line Chart','Bar Chart','Scatter plot','Pie Chart','Histogram','Box plot','HeatMap','Pair plot'],index=None,placeholder="Choose a chart")

    colors=px.colors.qualitative.Set2
    theme=st.selectbox("Choose Theme",["plotly","plotly_dark","ggplot2","seaborn"],index=0)

    num_cols=df.select_dtypes(include="number").columns
    cat_cols=df.select_dtypes(include='object').columns
    date_cols=df.select_dtypes(include='datetime').columns

    show_grid=st.toggle("Show Grid")
    
    if chart=="Line Chart":
        x_opt=list(num_cols)+list(date_cols)

        x_col=st.selectbox("Select X-axis",x_opt,index=None,placeholder="Choose a column")
        y_col = st.multiselect("Select Y-axis", num_cols, placeholder="Choose column(s)")

        if x_col and y_col:
            fig=px.line(df,x=x_col,y=y_col,color_discrete_sequence=colors)
            if chart not in ["Pie Chart","HeatMap","Pair plot"]:
                fig.update_xaxes(showgrid=show_grid)
                fig.update_yaxes(showgrid=show_grid)
            if title:
                fig.update_layout(title=title,template=theme)
            show_fig(fig)
    if chart=="Bar Chart":
        x_col=st.selectbox("Select X-axis",cat_cols,index=None,placeholder="Choose a column")
        y_col=st.selectbox("Select Y-axis",num_cols,index=None,placeholder="Choose a column")

        agg_func=st.selectbox("Aggregation",["sum","mean","count","min","max"])
        
        if x_col and y_col:
            grouped=df.groupby(by=x_col)[y_col].agg(agg_func).reset_index()
            fig=px.bar(grouped,x=x_col,y=y_col)
            if title:
                fig.update_layout(title=title,template=theme)
            show_fig(fig)

    if chart=="Scatter plot":
        x_col=st.selectbox("Select X-axis",num_cols,index=None,placeholder="Choose a column")
        y_col=st.selectbox("Select Y-axis",num_cols,index=None,placeholder="Choose a column")

        trend=st.toggle("TrendLine")
        color_col=st.selectbox("Select column to color",df.columns,index=None,placeholder="Choose a column to color")
        if x_col and y_col:

            if trend and color_col:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col, trendline="ols")
            elif trend:
                fig = px.scatter(df, x=x_col, y=y_col, trendline="ols")
            elif color_col:
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col)
            else:
                fig = px.scatter(df, x=x_col, y=y_col)
            fig.update_layout(template=theme)
            if title:
                fig.update_layout(title=title)
            show_fig(fig)

    if chart=="Histogram":
        x_col=st.selectbox("Select X-axis",num_cols,index=None,placeholder="Choose a column")
        bins=st.slider("Choose bins",5,100)
        if x_col:
            fig=px.histogram(df,x=x_col,nbins=bins,color_discrete_sequence=colors)
            fig.update_layout(template=theme)
            if title:
                fig.update_layout(title=title)
            show_fig(fig)
    if chart=="Box plot":
        y_col=st.selectbox("Select Y-axis",num_cols,index=None,placeholder="Choose a column")
        x_col=st.selectbox("Select X-axis(optional)",[None]+list(cat_cols))

        if y_col:
            if x_col:
                fig=px.box(df,x=x_col,y=y_col,color_discrete_sequence=colors)
            else:
                fig=px.box(df,y=y_col,color_discrete_sequence=colors)
            fig.update_layout(template=theme)
            if title:
                fig.update_layout(title=title)
            show_fig(fig)
    if chart=="HeatMap":
        fig=px.imshow(df.select_dtypes(include="number").corr(),text_auto=True,color_continuous_scale="Greens")
        fig.update_layout(template=theme)
        if title:
            fig.update_layout(title=title)
        show_fig(fig)

    if chart=="Pie Chart":
        x_col=st.selectbox("Select X-axis",cat_cols,index=None,placeholder="Choose a column")
        y_col=st.selectbox("Select Y-axis",num_cols,index=None,placeholder="Choose a column")

        if x_col and y_col:
            fig=px.pie(df,names=x_col,values=y_col)
            fig.update_layout(template=theme)
            if title:
                fig.update_layout(title=title)
            show_fig(fig)
    if chart=="Pair plot":
        fig=px.scatter_matrix(df,dimensions=num_cols,color_discrete_sequence=colors)
        fig.update_layout(template=theme)
        if title:
            fig.update_layout(title=title)
        show_fig(fig)