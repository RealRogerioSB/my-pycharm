from datetime import datetime

import requests
import streamlit as st

st.set_page_config(
    page_title="Streamlit Apps",
    layout="wide",
)

with open("styles/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.header(":material/logo_dev: Meus Apps")

col1, col2, col3 = st.columns(3, border=True)

with col1.expander("Cotação de Moedas Estrangeiras", icon="💰"):
    def format_date_br(date_default: str) -> str:
        return f"{datetime.strptime(date_default, format('%Y-%m-%d %H:%M:%S')):%d/%m/%Y %H:%M:%S}"


    with st.spinner("**Carregando, aguarde...**", show_time=True):
        get_cota_us = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL").json()
        get_cota_eu = requests.get("https://economia.awesomeapi.com.br/last/EUR-BRL").json()
        get_cota_gb = requests.get("https://economia.awesomeapi.com.br/last/GBP-BRL").json()

        st.caption("**:material/attach_money: Cotação do Dólar**")
        st.caption(f"Moeda $   : {get_cota_us['USDBRL']['name']}")
        st.caption(f"Data/Hora : {format_date_br(get_cota_us['USDBRL']['create_date'])}")
        st.caption(f"Valor (R$): {get_cota_us['USDBRL']['bid'].replace('.', ',')}")
        st.caption("")
        st.caption("**:material/euro: Cotação do Euro**")
        st.caption(f"Moeda $   : {get_cota_eu['EURBRL']['name']}")
        st.caption(f"Data/Hora : {format_date_br(get_cota_eu['EURBRL']['create_date'])}")
        st.caption(f"Valor (R$): {get_cota_eu['EURBRL']['bid'].replace('.', ',')}")
        st.caption("")
        st.caption("**:material/currency_pound: Cotação do Libra**")
        st.caption(f"Moeda $   : {get_cota_gb['GBPBRL']['name']}")
        st.caption(f"Data/Hora : {format_date_br(get_cota_gb['GBPBRL']['create_date'])}")
        st.caption(f"Valor (R$): {get_cota_gb['GBPBRL']['bid'].replace('.', ',')}")

with col2.expander("Markdown Incrível", icon="💯"):
    st.markdown("*Streamlit* é **realmente** ***legal***.")
    st.markdown("""
        :red[Streamlit] :orange[pode] :green[escrever] :blue[texto] :violet[em]
        :gray[belas] :rainbow[cores] e texto :blue-background[destacado].
    """)
    st.markdown("Here's a bouquet &mdash;"
                " :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")
