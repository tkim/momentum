import streamlit as st
import pandas as pd 
import base64
import matplotlib as plt
import seaborn as sns
import numpy as np 
import yfinance as yf 

st.title('Top 50 momentum stock in S&P 500')

st.markdown("""
This app shows the top 50 momentum stocks from S&P 500.
""")

st.sidebar.header('User Input')

# S&P 500 stocks
# web scrape vs. IEX API

# web scrape
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    dataframe = html[0]
    return dataframe

# IEX API - Batch Calls of 100

# Sidebar - Secotr selection
sorted_sector_unique = sorted(datafame['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering Data
dataframe_selected_sector = dataframe[(df['GICS Sector'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(dataframe_selected_sector.shape[0]) + 'rows and' + str(dataframe_selected_sector.shape[1]) + 'columns.')
st.dataframe(dataframe_selected_sector)


