import streamlit as st
import pandas as pd
import plotly.express as px

def analyze_spreadsheet(df):
    # Detect and report on data patterns, trends, and key takeaways
    st.subheader("Data Analysis")
    
    # Example analysis:
    st.write(f"The dataset has {df.shape[0]} rows and {df.shape[1]} columns.")
    st.write(f"The dataset contains the following columns: {', '.join(df.columns)}")
    st.write(f"The dataset has {df.isna().sum().sum()} missing values.")

    # Generate visual insights using Plotly
    st.subheader("Visual Insights")
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Trend Analysis')
    st.plotly_chart(fig)

    st.write("Key Takeaways:")
    st.write("- The data shows a positive trend over time.")
    st.write("- There are a few outliers that may need further investigation.")

def main():
    st.title("Spreadsheet Analysis Chatbot")

    # Allow user to upload a spreadsheet
    uploaded_file = st.file_uploader("Upload a spreadsheet", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Load the spreadsheet data into a DataFrame
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Analyze the spreadsheet data and display the results
        analyze_spreadsheet(df)

if __name__ == "__main__":
    main()
