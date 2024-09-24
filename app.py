import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import LlamaForCausalLM, LlamaTokenizer
import groq

# Initialize the Groq client and the llama3-8b-8192 model
groq_client = groq.Groq(api_key=st.secrets["GROQ_KEY"])
model = LlamaForCausalLM.from_pretrained("decapoda-research/llama3-8b-8192")
tokenizer = LlamaTokenizer.from_pretrained("decapoda-research/llama3-8b-8192")

def chatbot_response(user_input, df):
    # Use the Groq client and the llama3-8b-8192 model to generate a response
    prompt = f"User: {user_input}\nAssistant: Let me analyze the provided spreadsheet to help answer your question. Here's what I found:"
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output = model.generate(input_ids, max_length=1024, num_return_sequences=1, do_sample=True, top_k=50, top_p=0.95, num_beams=5)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    # Perform additional analysis and generate visualizations based on the user's input
    takeaways = analyze_spreadsheet(df)
    response += "\n\nKey Takeaways:\n"
    for takeaway in takeaways:
        response += f"- {takeaway}\n"

    return response

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

    # Generate visual insights using Plotly
    st.subheader("Visual Insights")
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Trend Analysis')
    st.plotly_chart(fig)

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
            chatbot_response = chatbot_response(user_input, df)
            st.write(chatbot_response)

if __name__ == "__main__":
    main()
