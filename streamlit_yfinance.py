import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Gráficos de Ações", layout="wide")


@st.cache_data(show_spinner=False)
def load_data(tickers):
    data_ticker = yf.Tickers(" ".join(tickers))
    cota = data_ticker.history(period="1d", start="2010-01-01", end=pd.to_datetime("today"))
    return cota["Close"]


with st.spinner("Aguarde enquanto carrega os dados..."):
    data = load_data(["AAPL", "ABEV3.SA", "BBAS3.SA", "GGBR4.SA", "ITUB4.SA", "NVDA", "PETR4.SA", "VALE3.SA"])

    st.markdown("## Preço de Ações")
    st.markdown("### O gráfico abaixo representa a evolução do preço das ações ao longo dos anos")

    st.sidebar.header("Filtros")

    list_tickers = st.sidebar.multiselect(label="Escolha as ações para visualizar:", options=data.columns,)

    if list_tickers:
        data = data[list_tickers]
        if not data.empty:
            data = data.rename(columns={list_tickers[0]: "Close"})

            date_min = data.index.min().to_pydatetime()
            date_max = data.index.max().to_pydatetime()

            interval = st.sidebar.slider(
                label="Selecione o período",
                min_value=date_min,
                max_value=date_max,
                value=(date_min, date_max),
                format="DD/MM/YYYY"
            )

            data = data[interval[0]:interval[1]]

            st.sidebar.write(f"Período: {interval[0]:%d/%m/%Y} a {interval[1]:%d/%m/%Y}")

            st.line_chart(data)
    else:
        st.toast("Não há dados para visualizar o gráfico", icon="📊")
