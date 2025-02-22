from datetime import timedelta

import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Página Principal", layout="wide")


@st.cache_data
def load_data(tickers):
    data_ticker = yf.Tickers(" ".join(tickers))
    cota = data_ticker.history(period="1d", start="2010-01-01", end=pd.to_datetime("today"))
    return cota["Close"]


data = load_data(["AAPL", "ABEV3.SA", "BBAS3.SA", "GGBR4.SA", "ITUB4.SA", "NVDA", "PETR4.SA", "VALE3.SA"])

st.write("""
Preço de Ações
O gráfico abaixo representa a evolução do preço das ações ao longo dos anos
""")

st.sidebar.header("Filtros")

list_tickers = st.sidebar.multiselect(label="Escolha as ações para visualizar:", options=data.columns)

if list_tickers:
    data = data[list_tickers]
    if len(list_tickers) == 1:
        data = data.rename(columns={list_tickers[0]: "Close"})

date_min = data.index.min().to_pydatetime()
date_max = data.index.max().to_pydatetime()

interval = st.sidebar.slider("Selecione o período", min_value=date_min, max_value=date_max,
                             value=(date_min, date_max), step=timedelta(days=1), format="DD/MM/YYYY")

data = data[interval[0]:interval[1]]

st.sidebar.write(f"Período: {interval[0]:%d/%m/%Y} a {interval[1]:%d/%m/%Y}")

st.line_chart(data)
