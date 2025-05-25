from datetime import datetime

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Streamlit Apps",
    layout="wide",
)

with open("styles/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("#### :material/logo_dev: Meus Apps")

col1, col2, col3 = st.columns(3, border=True)

with col1.expander("Cotação de Moedas Estrangeiras", icon="💰"):
    def format_date_br(date_default: str) -> str:
        return f"{datetime.strptime(date_default, format('%Y-%m-%d %H:%M:%S')):%d/%m/%Y %H:%M:%S}"


    with st.spinner("**Carregando, aguarde...**", show_time=True):
        get_cota_us = pd.DataFrame([requests.get("https://economia.awesomeapi.com.br/last/USD-BRL").json()["USDBRL"]])
        get_cota_us = get_cota_us[["name", "create_date", "bid"]]

        get_cota_eu = pd.DataFrame([requests.get("https://economia.awesomeapi.com.br/last/EUR-BRL").json()["EURBRL"]])
        get_cota_eu = get_cota_eu[["name", "create_date", "bid"]]

        get_cota_gb = pd.DataFrame([requests.get("https://economia.awesomeapi.com.br/last/GBP-BRL").json()["GBPBRL"]])
        get_cota_gb = get_cota_gb[["name", "create_date", "bid"]]

        cota = pd.concat([get_cota_us, get_cota_eu, get_cota_gb])
        cota["name"] = cota["name"].apply(lambda x: x.replace("/Real Brasileiro", ""))

        st.dataframe(
            data=cota,
            hide_index=True,
            use_container_width=True,
            column_config={
                "name": st.column_config.TextColumn("Moeda $"),
                "create_date": st.column_config.DateColumn("Data/Hora", format="DD/MM/YYYY"),
                "bid": st.column_config.NumberColumn("Valor R$", format="dollar"),
            },
        )

with col2.expander("Markdown Incrível", icon="💯"):
    st.markdown("*Streamlit* é **realmente** ***legal***.")
    st.markdown("""
        :red[Streamlit] :orange[pode] :green[escrever] :blue[texto] :violet[em]
        :gray[belas] :rainbow[cores] e texto :blue-background[destacado].
    """)
    st.markdown("Here's a bouquet &mdash;"
                " :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

with col3.expander("Valor por extenso", icon="💯"):
    def num_extenso(n: int) -> str:
        unidade = ["zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
        dez_x = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove"]
        dezena = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa", "cem"]

        return dezena[n // 10] + " e " + unidade[n % 10] \
            if n >= 20 and n % 10 != 0 else dezena[n // 10] \
            if n >= 20 and n % 10 == 0 else dez_x[n % 10] \
            if 10 <= n < 20 and n % 10 == 0 else dez_x[n - 10] \
            if 10 <= n < 20 and n % 10 != 0 else unidade[n] \
            if n < 10 and n % 10 != 0 else unidade[0]


    st.number_input("Digite um número entre 0 e 100:", min_value=0, max_value=100, value=0, key="num_extenso")

    st.markdown("")

    st.columns([1, 2, 1])[1].button("**Converter**", key="extenso", type="primary", icon=":material/pin:",
                                    use_container_width=True)

    st.markdown("")

    if st.session_state["extenso"]:
        st.markdown(f"O número por extenso é {num_extenso(st.session_state['num_extenso'])}.")
