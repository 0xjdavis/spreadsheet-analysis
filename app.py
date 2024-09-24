import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import groq
from datetime import datetime

# Initialize the Groq client and the llama3-8b-8192 model
groq_client = groq.Groq(api_key=st.secrets["GROQ_KEY"])

# Select Groq Model
model = st.sidebar.selectbox(
    "Select a model:",
    ("llama3-8b-8192", "llama3-groq-70b-8192-tool-use-preview", "mixtral-8x7b-32768", "gemma-7b-it"),
)

system_prompt = '''
You are the world's best data analysts. You are not only an INTP making up a small percentage of the personalities, but you are specially trained in graphic design and engineering. Your clients include Apple, Microsoft and you were awarded recently for your contributions to the field of User Experience Design by Jakob Nielsen.
You have access to python library (pychart) and are a master designer when it comes to visualizing data in the form of data driven dashboards.
You can visualize data and flow using code interpreter and js librarires.

Help me make sense of this spreadsheet.
It is a list of people that hasve contacted us about tutoring and scheduled a call who purchased.
This needs to be visualised in a chart over time.

Create a dashboard where the top panel extends the entire witdth of the page but only half the height of the page.
Fill that section of the page with whatever chart you think will tell the best story reflecting the data.
The second half of the page should be divided into three different sections showing three KPI.
- KPI 1 Top 10 individuals who purchased the most over time ranked, from most to least.
- KPI 2 Top 10 law schools attended by people who purchased the most over time, ranked from most to least.
- KPI 3 Top 10 countries that individuals who purchased the most over time were from, ranked from most to least.

Look at the funnel over time.
- Identify trends and highlight them in your charts
- Display what is obvious.
- Display what is not obvious. Remember you see things others do not. Look harder to identify patterns.

Are we getting more or less inquiries scheduled per inquiry, purchase per call/inquirey, etc...
Tell me what is and is not obvious.
'''

def analyze_spreadsheet(df):
    # Detect and report on data patterns, trends, and key takeaways
    st.subheader("Data Analysis")
    
    # Example analysis:
    row_count = df.shape[0]
    col_count = df.shape[1]
    missing_values = df.isna().sum().sum()

    st.write(f"The dataset has {row_count} rows and {col_count} columns.")
    st.write(f"The dataset contains the following columns: {', '.join(df.columns)}")
    st.write(f"The dataset has {missing_values} missing values.")

    # Convert the date column to datetime
    df[df.columns[0]] = pd.to_datetime(df[df.columns[0]])

    # Generate visual insights using Plotly
    st.subheader("Visual Insights")

    # Top panel - Trend Analysis
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Trend Analysis')
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

    # Generate dynamic key takeaways
    takeaways = []
    if row_count > 1000:
        takeaways.append("The dataset is quite large, with over 1,000 rows. This may require additional processing power or sampling to analyze efficiently.")
    if missing_values > 0:
        takeaways.append(f"The dataset contains {missing_values} missing values, which may need to be handled before further analysis.")
    if df[df.columns[1]].std() > 1000:
        takeaways.append("The data shows high variability in the second column, which could indicate the presence of outliers or unusual data points.")
    if df[df.columns[1]].mean() > 10000:
        takeaways.append("The average value in the second column is quite high, suggesting the data may represent high-value items or transactions.")

    return takeaways

def main():
    st.title("Spreadsheet Analysis Chatbot")

    # Display system prompt
    st.markdown(system_prompt)

    # Allow user to upload a spreadsheet
    uploaded_file = st.file_uploader("Upload a spreadsheet", type=["xlsx", "csv"])

    if uploaded_file is not None:
        # Load the spreadsheet data into a DataFrame
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Add chatbot functionality
        user_input = st.text_input("Ask me anything about the spreadsheet:", "")
        if user_input:
            response = "Let me analyze the provided spreadsheet to help answer your question. Here's what I found:\n\n"
            takeaways = analyze_spreadsheet(df)
            response += "Key Takeaways:\n"
            for takeaway in takeaways:
                response += f"- {takeaway}\n"
            st.write(response)

if __name__ == "__main__":
    main()
