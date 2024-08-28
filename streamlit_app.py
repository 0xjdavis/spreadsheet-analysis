import pandas as pd
import streamlit as st
import plotly.express as px

import time

from openai import OpenAI
openai_api_key = st.secrets["openai_key"]
client = OpenAI(api_key=openai_api_key)

import base64

from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

from collections import Counter

import matplotlib 
import matplotlib.pyplot as plt

matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as funcAnimation
 

# Setting page layout
st.set_page_config(
    page_title="Data Visualization Analysis Chatbot with Langchain, OpenAI and a Plotly 3D Scatterplot of CSV Data",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar for API Key and User Info
st.sidebar.header("About App")
st.sidebar.markdown('This is a data visualization analysis chatbot using Plotly, LangChain, and OpenAI GPT 3.5 model to analyze data from a CSV created by <a href="https://ai.jdavis.xyz" target="_blank">0xjdavis</a>.', unsafe_allow_html=True)

# Calendly
st.sidebar.markdown("""
    <hr />
    <center>
    <div style="border-radius:8px;padding:8px;background:#fff";width:100%;">
    <img src="https://avatars.githubusercontent.com/u/98430977" alt="Oxjdavis" height="100" width="100" border="0" style="border-radius:50%"/>
    <br />
    <span style="height:12px;width:12px;background-color:#77e0b5;border-radius:50%;display:inline-block;"></span> <b style="color:#000000">I'm available for new projects!</b><br />
    <a href="https://calendly.com/0xjdavis" target="_blank"><button style="background:#126ff3;color:#fff;border: 1px #126ff3 solid;border-radius:8px;padding:8px 16px;margin:10px 0">Schedule a call</button></a><br />
    </div>
    </center>
    <br />
""", unsafe_allow_html=True)

# Copyright
st.sidebar.caption("©️ Copyright 2024 J. Davis")


st.title('Langchain & OpenAI Chatbot with Plotly 3D Scatterplot of CSV Data')
st.caption('')
st.write('''
    This 3D scatterplot is based on 92 Oncology companies. Only 16 of have passed Phase 2 trial 
    with a market cap of 50-300 Million and have at least one well known major investor.
''')


# ----------------------------------------------
# PLOTLY VISUALIZATION
# CSV DATA SOURCE
df = pd.read_csv(r'csv/investors.csv',index_col=[0])

fig = px.scatter_3d(
  df,
  x="Enterprise Value",
  y="Cash and Marketable",
  z="Cash Burn (Runway)",
  color='Company'
)
fig.update_layout(
   height=550
)
fig.update_scenes(
  camera_eye_x=1.2,
  camera_eye_y=1.2,
  camera_eye_z=1.2,
  camera_center_z=-0.5,
  camera_center_y=-0.1
)
#fig.show()
st.plotly_chart(fig)

# ----------------------------------------------
# Assuming 'df' is your pandas DataFrame and 'Marketcap' is the column of interest.
# You would replace 'Company' with the column you want to use as labels.

# Create a pie chart using the 'Marketcap' column
plt.figure(figsize=(8, 8))
plt.pie(df['Marketcap'], labels=df['Company'], autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title('Market Capitalization by Company')
plt.show()

# ----------------------------------------------
# SHOW CSV DATA FOR CASH IN A PIE CHART
with st.expander('View Data'):
  st.write(df)

with st.expander('View Investor Frequency'):
  # Splitting investor names and storing them in a list
  investor_score_lists = df['Investor Score'].tolist()
  #investor_score_lists = investor_score_lists.split(investor_score_lists).tolist()
  investors_lists = df['Top Investors'].str.split(' n/a ').tolist()
  #st.write(investor_lists)
  # Flattening the list of lists into a single list of investors
  investors = [investor for sublist in investors_lists for investor in sublist]
  #st.write(investors)
  # Counting investor names. This will also count n/a values
  investor_counts = Counter(investors)
  #st.write(investor_counts)
  # Removing the 'n/a' key
  investor_counts.pop('n/a', None)
  # Filtering investors who invest in more than one company
  top_investors_multiple_companies = {
    investor: count for investor,
    count in investor_counts.items() if count > 1
  }
  #st.write(top_investors_multiple_companies)
  company_list = investors_lists
  query_company = st.selectbox('Select an invstor:', investors, disabled=not investors)
  investment_frequency = df[df['Top Investors'].str.contains(query_company, na=False)]['Company']
  st.write(investment_frequency)

# ----------------------------------------------
# IMAGE
# st.image("csv/investors.png")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "csv/investors.png"

# Getting the base64 string
base64_image = encode_image(image_path)

# ----------------------------------------------
# GPT-4-Vision ANALYSIS OF LLM STOCK IMAGE
if "messages" not in st.session_state:
    # ----------------------------------------------
    # client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are a financial analyst. This is a 3D Scatterplot of Companies. Only 16 of which that have passed Phase 2 trial and are between 50-300 Million market cap with at least one well known major investor. Tell me some details about how this scatterplot could be improved."},
                    {
                        "type": "image_url",
                        "image_url": {
                          "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                        #image_url": "https://imgs.search.brave.com/TZhCPTYpZf3nanAYZb3qpulr8YD8j83iA4RmMf7Ilxc/rs:fit:860:0:0/g:ce/aHR0cHM6Ly92aXNt/ZS5jby9ibG9nL3dw/LWNvbnRlbnQvdXBs/b2Fkcy8yMDE3LzA3/L1NjaWVuY2UtU3Bo/ZXJpY2FsLUNvbnRv/dXItR3JhcGhzLmpw/Zw",
                    },
                ],
            },
        ],
        max_tokens=1000,
    )
    msg = response.choices[0].message.content

    with st.spinner('Running the model...'):
      #time.sleep(5)
      #st.success('Done!')
      st.session_state["messages"] = [{"role": "assistant", "content": msg}]

# ----------------------------------------------
# CTA BUTTON
#url = "/Chart%20Analysis%20Chatbot%20(GPT-4-Vision)"
#st.markdown(
#    f'<div><a href="{url}" target="_self" style="justify-content:center; padding: 10px 10px; background-color: #2D2D2D; color: #efefef; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px;">Analyze Chart</a></div>',
#        unsafe_allow_html=True
#    )

# ----------------------------------------------
# RENDER MESSAGE
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ----------------------------------------------
# CHATBOT
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # INSERT LANGCHAIN AGENT
    llm = ChatOpenAI(model_name='gpt-4o-mini', temperature=1, openai_api_key=openai_api_key)
    agent = create_pandas_dataframe_agent(llm, df, verbose=True, agent_type=AgentType.OPENAI_FUNCTIONS, allow_dangerous_code=True)
    response = agent.run(prompt)

    #response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #msg = response.choices[0].message.content
    msg = response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

