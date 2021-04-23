import streamlit as st
import pandas as pd 
import base64
import matplotlib.pyplot as plt
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

dataframe = load_data()
sector = dataframe.groupby('GICS Sector')

# IEX API - Batch Calls of 100

# Sidebar - Secotr selection
sorted_sector_unique = sorted(dataframe['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering Data
dataframe_selected_sector = dataframe[(dataframe['GICS Sector'].isin(selected_sector))]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(dataframe_selected_sector.shape[0]) + 'rows and' + str(dataframe_selected_sector.shape[1]) + 'columns.')
st.dataframe(dataframe_selected_sector)

# Download S&P 599 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(dataframe):
    csv = dataframe.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # strings <>bytes conversion
    href = f'<a href="data:file/csv;base64{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(dataframe_selected_sector), unsafe_allow_html=True)

data = yf.download(
    tickers=list(dataframe_selected_sector[:10].Symbol),
    period='ytd',
    interval='1d',
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
)

# Plot closing price
def price_plot(symbol):
    dataframe = pd.DataFrame(data[symbol].Close)
    dataframe['Date'] = dataframe.index
    plt.fill_between(dataframe.Date, dataframe.Close, color='skyblue', alpha=0.3)
    plt.plot(dataframe.Date, dataframe.Close, color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(dataframe_selected_sector.Symbol)[:num_company]:
        price_plot(i)
