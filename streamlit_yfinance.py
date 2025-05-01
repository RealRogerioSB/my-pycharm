import pandas as pd
import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Gráficos de Ações", layout="wide")


@st.cache_data(show_spinner=False)
def load_data(tickers: list[str]) -> pd.DataFrame:
    data_ticker: yf.Tickers = yf.Tickers(" ".join(tickers))
    cota: pd.DataFrame = data_ticker.history(period="1d", start="2010-01-01", end=pd.to_datetime("today"))
    return cota["Close"]


with st.spinner("Aguarde enquanto carrega os dados...", show_time=True):
    data = load_data(["AAPL", "ABEV3.SA", "BBAS3.SA", "GGBR4.SA", "ITUB4.SA", "NVDA", "PETR4.SA", "VALE3.SA"])

    st.markdown("## Preço de Ações")
    st.markdown("### O gráfico abaixo representa a evolução do preço das ações ao longo dos anos")
    st.sidebar.markdown("## Filtros")

    st.sidebar.multiselect(label="Escolha as ações para visualizar:", options=data.columns,
                           key="list_tickers", placeholder="Escolha uma opção")

    if st.session_state["list_tickers"]:
        data: pd.DataFrame = data[st.session_state["list_tickers"]]
        if not data.empty:
            date_min = data.index.min().to_pydatetime()
            date_max = data.index.max().to_pydatetime()

            st.sidebar.slider(
                label="Selecione o período",
                key="interval",
                min_value=date_min,
                max_value=date_max,
                value=(date_min, date_max),
                format="DD/MM/YYYY"
            )

            data = data[st.session_state["interval"][0]:st.session_state["interval"][1]]

            st.sidebar.write(f"Período: {st.session_state["interval"][0]:%d/%m/%Y} "
                             f"a {st.session_state["interval"][1]:%d/%m/%Y}")

            st.line_chart(data)
        else:
            st.toast("Não há dados para visualizar o gráfico", icon="📊")
