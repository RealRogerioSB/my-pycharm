import locale
from datetime import date

import pandas as pd
import streamlit as st
from streamlit.connections import SQLConnection

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

st.set_page_config(page_title="Contracheque BB", layout="wide")

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)

st.header("💰Contracheque BB")


# captura o último período
@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def last_period() -> int:
    return engine.query(
        sql="SELECT DISTINCT MAX(período) AS MAX_PERIOD FROM espelho",
        show_spinner=False,
        ttl=60
    )["max_period"].iloc[0]


take_year: int = int(last_period() / 100)
take_month: int = last_period() % 100


# extrato mensal
@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_extract_monthly(receive_year: int, receive_month: int) -> pd.DataFrame:
    return engine.query(
        sql="""SELECT l.lançamento, e.período, e.acerto, e.valor
               FROM espelho e INNER JOIN lançamento l ON l.id_lançamento = e.id_lançamento
               WHERE e.período / 100 = :get_year
                 AND e.período % 100 = :get_month
               ORDER BY e.período, e.acerto DESC, e.valor DESC""",
        show_spinner=False,
        ttl=60,
        params=dict(get_year=receive_year, get_month=receive_month),
    )


# extrato anual
@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_extract_annual(receive_year: int) -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT l.lançamento, e.período, e.acerto, e.valor
               FROM espelho e INNER JOIN lançamento l ON l.id_lançamento = e.id_lançamento
               WHERE e.período / 100 = :get_year""",
        show_spinner=False,
        ttl=60,
        params=dict(get_year=receive_year),
    )
    load["período"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%m").astype(int)
    load = load.pivot(index=["lançamento", "acerto"], columns="período", values="valor") \
        .reset_index() \
        .set_index(["lançamento"]) \
        .fillna(value=0) \
        .rename(columns={1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
                         7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"})
    load["Média"] = load[load.columns[1:]].mean(axis=1)
    load["Total"] = load[load.columns[1:-1]].sum(axis=1)
    load = load.sort_values(by=["acerto", "Total"], ascending=[False, False])

    return load


# total anual
@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_total_annual() -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT e.período, SUM(e.valor) AS valor
               FROM espelho e
               GROUP BY e.período
               ORDER BY e.período""",
        show_spinner=False,
        ttl=60,
    )
    load["ano"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%Y")
    load["mês"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%b")
    load = load.groupby(["ano", "mês"])["valor"].sum() \
        .reset_index() \
        .pivot(index="ano", columns="mês", values="valor") \
        .fillna(0)[["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]]
    load["Média"] = load.mean(axis=1)
    load["Total"] = load[load.columns[:-1]].sum(axis=1)

    return load


# gráfico anual
@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_graphic_annual(receive_year: int) -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT e.período, SUM(e.valor) AS valor
               FROM espelho e
               WHERE e.período / 100 = :get_year
               GROUP BY e.período
               ORDER BY e.período""",
        show_spinner=False,
        ttl=60,
        params=dict(get_year=receive_year),
    )
    load["mês"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%b")
    load = load.pivot(columns="mês", values="valor").reset_index()

    return load


tab1, tab2, tab3, tab4 = st.tabs(["**Extrato Mensal**", "**Extrato Anual**", "**Total Anual**", "**Gráfico**"])

with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        mes: int = st.slider(label="**Mês:**", min_value=1, max_value=12, value=take_month, key="slider_months")

        ano: int = st.columns(3)[0].selectbox(
            label="**Ano:**",
            options=range(date.today().year, 2004, -1),
            index=0 if take_year == date.today().year else 1,
            key="select_years"
        )

    with col2:
        df1: pd.DataFrame = load_extract_monthly(ano, mes)
        df1.columns = [str(column).capitalize() for column in df1.columns]
        df1["Período"] = pd.to_datetime(df1["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df1,
            height=318,
            use_container_width=True,
            hide_index=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")},
            row_height=28,
            key="editor_months"
        )

with tab2:
    anual: int = st.slider(
        label="**Ano:**",
        min_value=2005,
        max_value=date.today().year,
        value=take_year,
        key="slider_years"
    )

    df2: pd.DataFrame = load_extract_annual(anual)
    df2.columns = [str(column).capitalize() for column in df2.columns]
    df2.index.rename("Lançamento", inplace=True)

    st.data_editor(
        data=df2,
        height=318,
        use_container_width=True,
        column_config={key: st.column_config.NumberColumn(format="dollar")
                       for key in df2.columns if key not in ["Acerto"]},
        row_height=28,
        key="editor_years"
    )

with tab3:
    df3: pd.DataFrame = load_total_annual()

    with st.container():
        st.data_editor(
            data=df3,
            use_container_width=True,
            column_config={key: st.column_config.NumberColumn(format="dollar") for key in df3.columns},
            row_height=28,
        )

with tab4:
    slider_graphic: int = st.slider(
        label="**Ano:**",
        min_value=2005,
        max_value=date.today().year,
        value=take_year,
        key="slider_graphic"
    )

    df4: pd.DataFrame = load_graphic_annual(slider_graphic)

    st.bar_chart(data=df4)
