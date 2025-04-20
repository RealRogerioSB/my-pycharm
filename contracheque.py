import locale
from datetime import date

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from streamlit.connections import SQLConnection

st.set_page_config(page_title="Contracheque BB", layout="wide")

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

st.header("💰Contracheque BB")

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)


@st.cache_resource(show_spinner="⏳Atualizando os dados, aguarde...")
def load_and_save(csv_file: str) -> int:
    return pd.read_csv(
        filepath_or_buffer=csv_file,
        engine="pyarrow"
    ).to_sql(
        name="espelho",
        con=engine,
        if_exists="append",
        index=False
    )


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def import_period() -> int:
    df = engine.query(
        sql="SELECT MAX(período) AS max_period FROM espelho",
        show_spinner=False,
        ttl=60
    )
    return df["max_period"].values[0]


max_period: int = import_period()

if "csv_file" not in st.session_state:
    st.session_state["csv_file"] = None

# inserir novos registros para a tabela espelho
st.session_state["csv_file"] = st.columns(3)[0].file_uploader("Importar", type="csv", label_visibility="hidden")

if st.session_state["csv_file"] and st.session_state["csv_file"].name == "espelho.csv":
    try:
        saves: int = load_and_save(st.session_state["csv_file"])

        if saves is None:
            st.toast("**Não houve registros para atualizar o espelho...**", icon=":material/error:")
            st.stop()

        st.toast(f"**Atualização do mês salvou {saves} registros com sucesso**", icon=":material/check_circle:")

    except FileNotFoundError:
        st.toast("**Falha ao localizar o arquivo do espelho...**", icon=":material/error:")
        st.stop()


@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_months(_year: int, _month: int) -> pd.DataFrame:
    return engine.query(
        sql="""SELECT t2.lançamento,
                      t1.período,
                      t1.acerto,
                      t1.valor
               FROM espelho t1
                        INNER JOIN lançamento t2
                                   ON t2.id_lançamento = t1.id_lançamento
               WHERE t1.período / 100 = :year
                 AND t1.período % 100 = :month
               ORDER BY t1.período,
                        t1.acerto DESC,
                        t1.valor DESC""",
        show_spinner=False,
        ttl=60,
        params=dict(_year=_year, _month=_month),
    )


@st.cache_data(show_spinner="**⏳Obtendo os dados, aguarde...**")
def load_annual(_year: int) -> pd.DataFrame:
    return engine.query(
        sql="""SELECT t2.lançamento,
                      t1.período,
                      t1.acerto,
                      t1.valor
               FROM espelho t1
                        INNER JOIN lançamento t2
                                   ON t2.id_lançamento = t1.id_lançamento
               WHERE t1.período / 100 = :_year
               ORDER BY t1.período,
                        t1.acerto DESC,
                        t1.valor DESC""",
        show_spinner=False,
        ttl=60,
        params=dict(_year=_year),
    )


tab1, tab2 = st.tabs(["**Mensal**", "**Anual**"])

with tab1:
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        mes: int = st.slider(label="**Mês:**", min_value=1, max_value=12, value=max_period % 100)

        ano: int = st.columns(3)[0].selectbox(label="**Ano:**", options=range(date.today().year, 2004, -1))

    with col2:
        df1: pd.DataFrame = load_months(ano, mes)
        df1.columns = [str(column).capitalize() for column in df1.columns]
        df1["Período"] = pd.to_datetime(df1["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df1,
            use_container_width=True,
            hide_index=True,
            column_config={
                "lançamento": st.column_config.TextColumn(label="Lançamento"),
                "período": st.column_config.NumberColumn(label="Período"),
                "acerto": st.column_config.CheckboxColumn(label="Acerto"),
                "valor": st.column_config.NumberColumn(label="Valor", format="dollar")
            }
        )

with tab2:
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        anual: int = st.slider(label="**Ano:**", min_value=2005, max_value=date.today().year, value=max_period / 100)

    with col2:
        df2: pd.DataFrame = load_annual(anual)
        df2.columns = [str(column).capitalize() for column in df2.columns]
        df2["Período"] = pd.to_datetime(df2["Período"], format="%Y%m").dt.strftime("%B de %Y")

        st.data_editor(
            data=df2, hide_index=True, use_container_width=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")}
        )
