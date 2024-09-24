import streamlit as st
import pandas as pd
import plotly.express as px
import groq
from datetime import datetime

# Initialize the Groq client and the llama3-8b-8192 model
groq_client = groq.Groq(api_key=st.secrets["GROQ_KEY"])

# Select Groq Model
model = st.sidebar.selectbox(
    "Select a model:",
    ("llama3-8b-8192", "llama3-groq-70b-8192-tool-use-preview", "mixtral-8x7b-32768", "gemma-7b-it"),
)

# System prompt for display
system_prompt = '''
You are the world's best data analysts. You are not only an INTP making up a small percentage of the personalities, 
but you are specially trained in graphic design and engineering. 
Your clients include Apple, Microsoft, and you were awarded recently for your contributions to the field of User Experience Design by Jakob Nielsen.
You can visualize data and flow using code interpreter and JS libraries.

Help me make sense of this spreadsheet.
It is a list of people who have contacted us about tutoring and scheduled a call who purchased.
This needs to be visualized in a chart over time, along with three KPIs.
'''

def analyze_spreadsheet(df):
    """Analyze the spreadsheet data and generate insights and visualizations."""
    st.subheader("Data Analysis")

    # Display basic data information
    row_count = df.shape[0]
    col_count = df.shape[1]
    missing_values = df.isna().sum().sum()

    st.write(f"The dataset has {row_count} rows and {col_count} columns.")
    st.write(f"Columns: {', '.join(df.columns)}")
    st.write(f"Missing values: {missing_values}")

    # Ensure the first column is a valid datetime format
    try:
        df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])
        st.write("Successfully parsed the date column.")
    except Exception as e:
        st.write(f"Error parsing the date column: {e}")
        return None

    # Generate visual insights using Plotly
    st.subheader("Visual Insights")

    # Top panel - Trend Analysis (Time Series)
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Trend Analysis Over Time')
    st.plotly_chart(fig, use_container_width=True)

    # Lower panel - KPI visualizations
    col1, col2, col3 = st.columns(3)

    # KPI 1 - Top 10 individuals who purchased the most
    with col1:
        st.subheader("Top 10 Purchasers")
        top_purchasers = df.groupby(df.columns[2]).size().sort_values(ascending=False).head(10)
        fig = px.bar(top_purchasers, x=top_purchasers.index, y=top_purchasers.values)
        st.plotly_chart(fig, use_container_width=True)

    # KPI 2 - Top 10 law schools attended
    with col2:
        st.subheader("Top 10 Law Schools")
        top_law_schools = df.groupby(df.columns[3]).size().sort_values(ascending=False).head(10)
        fig = px.bar(top_law_schools, x=top_law_schools.index, y=top_law_schools.values)
        st.plotly_chart(fig, use_container_width=True)

    # KPI 3 - Top 10 countries
    with col3:
        st.subheader("Top 10 Countries")
        top_countries = df.groupby(df.columns[4]).size().sort_values(ascending=False).head(10)
        fig = px.bar(top_countries, x=top_countries.index, y=top_countries.values)
        st.plotly_chart(fig, use_container_width=True)

    # Generate key takeaways dynamically
    takeaways = []
    if row_count > 1000:
        takeaways.append("The dataset is large, with over 1,000 rows, which may require more processing.")
    if missing_values > 0:
        takeaways.append(f"There are {missing_values} missing values.")
    if df[df.columns[1]].std() > 1000:
        takeaways.append("High variability detected in the data, suggesting potential outliers.")
    if df[df.columns[1]].mean() > 10000:
        takeaways.append("The average value is high, indicating high-value items or transactions.")

    return takeaways

def main():
    st.title("Spreadsheet Analysis Chatbot")

    # Display the system prompt
    st.markdown(system_prompt)

    # Allow the user to upload a spreadsheet
    uploaded_file = st.file_uploader("Upload a spreadsheet", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Load the spreadsheet data into a DataFrame
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # User input for specific questions about the data
        user_input = st.text_input("Ask me anything about the spreadsheet:", "")

        if user_input:
            st.write("Let me analyze the provided spreadsheet to help answer your question. Here's what I found:\n\n")
            with st.spinner("Analyzing the spreadsheet..."):
                takeaways = analyze_spreadsheet(df)

            if takeaways is not None:
                st.subheader("Key Takeaways")
                for takeaway in takeaways:
                    st.write(f"- {takeaway}")

if __name__ == "__main__":
    main()
