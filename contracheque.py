import locale
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit.connections import SQLConnection

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

st.set_page_config(page_title="Contracheque BB", layout="wide")

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)

st.header("💰Contracheque BB")


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def last_period() -> int:
    df = engine.query(
        sql="SELECT MAX(período) FROM espelho",
        show_spinner=False,
        ttl=60
    )
    return df.iloc[0, 0]


take_year: int = int(last_period() / 100)
take_month: int = last_period() % 100


@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_months(receive_year: int, receive_month: int) -> pd.DataFrame:
    return engine.query(
        sql="""SELECT t2.lançamento,
                      t1.período,
                      t1.acerto,
                      t1.valor
               FROM espelho t1
                    INNER JOIN lançamento t2
                               ON t2.id_lançamento = t1.id_lançamento
               WHERE t1.período / 100 = :get_year
                 AND t1.período % 100 = :get_month
               ORDER BY t1.período,
                        t1.acerto DESC,
                        t1.valor DESC""",
        show_spinner=False,
        ttl=60,
        params=dict(get_year=receive_year, get_month=receive_month),
    )


@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_annual(receive_year: int) -> pd.DataFrame:
    return engine.query(
        sql="""SELECT t2.lançamento,
                      t1.período,
                      t1.acerto,
                      t1.valor
               FROM espelho t1
                    INNER JOIN lançamento t2
                               ON t2.id_lançamento = t1.id_lançamento
               WHERE t1.período / 100 = :get_year
               ORDER BY t1.período,
                        t1.acerto DESC,
                        t1.valor DESC""",
        show_spinner=False,
        ttl=60,
        params=dict(get_year=receive_year),
    )


tab1, tab2 = st.tabs(["**Mensal**", "**Anual**"])

with tab1:
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        mes: int = st.slider(label="**Mês:**", min_value=1, max_value=12, value=take_month)

        ano: int = st.columns(3)[0].selectbox(
            label="**Ano:**",
            options=range(date.today().year, 2004, -1),
            index=0 if take_year == date.today().year else 1
        )

    with col2:
        df1: pd.DataFrame = load_months(ano, mes)
        df1.columns = [str(column).capitalize() for column in df1.columns]
        df1["Período"] = pd.to_datetime(df1["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df1,
            height=318,
            use_container_width=True,
            hide_index=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")},
            row_height=28
        )

with tab2:
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        anual: int = st.slider(
            label="**Ano:**",
            min_value=2005,
            max_value=date.today().year,
            value=take_year
        )

    with col2:
        df2: pd.DataFrame = load_annual(anual)
        df2.columns = [str(column).capitalize() for column in df2.columns]
        df2["Período"] = pd.to_datetime(df2["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df2,
            height=318,
            use_container_width=True,
            hide_index=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")},
            row_height=28
        )
