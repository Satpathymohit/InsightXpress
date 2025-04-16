import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="InsightXpress - EDA Tool", layout="wide")
st.title("📊 InsightXpress - Automated EDA Tool")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")

    # Show basic info
    st.subheader("🔍 Dataset Overview")
    st.write("Shape of Dataset:", df.shape)
    st.write("Preview:")
    st.dataframe(df.head())

    # Dataset summary
    st.subheader("📋 Summary Statistics")
    if st.checkbox("Show Data Types"):
        st.write(df.dtypes)

    if st.checkbox("Show Summary Statistics"):
        st.write(df.describe(include='all'))

    if st.checkbox("Show Missing Values"):
        st.write(df.isnull().sum())

    if st.checkbox("Show Duplicate Rows"):
        st.write("Duplicate Rows: ", df.duplicated().sum())

    # Column selector
    st.subheader("🧠 Column-wise Exploration")
    column = st.selectbox("Select a column to analyze", df.columns)

    if df[column].dtype == 'object' or df[column].nunique() < 30:
        st.write("🔢 Bar Chart of Top 20 Categories:")
        top_vals = df[column].value_counts(dropna=False).nlargest(20)
        fig = px.bar(top_vals, x=top_vals.index.astype(str), y=top_vals.values,
                     labels={'x': column, 'y': 'Count'})
        st.plotly_chart(fig)
    else:
        cleaned_col = pd.to_numeric(df[column], errors='coerce').dropna()

        st.write("📊 Histogram:")
        fig = px.histogram(cleaned_col, nbins=30, title=f"Histogram of {column}")
        st.plotly_chart(fig)

        st.write("📦 Boxplot:")
        fig2, ax = plt.subplots()
        sns.boxplot(x=cleaned_col, ax=ax)
        st.pyplot(fig2)

    # Correlation heatmap
    st.subheader("🔗 Correlation Heatmap")
    if st.checkbox("Show Correlation Heatmap"):
        numeric_df = df.select_dtypes(include=['number']).dropna()
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig4, ax = plt.subplots(figsize=(10, 5))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig4)
        else:
            st.warning("No numeric data available for correlation heatmap.")
else:
    st.info("👈 Please upload a CSV file to begin.")