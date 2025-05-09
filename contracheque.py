import locale
import time
from datetime import date

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib.container import BarContainer
from streamlit.connections import SQLConnection

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

st.cache_data.clear()

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)

sort_months: list[str] = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def get_release() -> dict[int: str]:
    load = engine.query(
        sql="SELECT id_lançamento, lançamento FROM lançamento ORDER BY lançamento",
        show_spinner=False,
        ttl=0
    )

    return {key: value for key, value in zip(load["id_lançamento"].to_list(), load["lançamento"].to_list())}


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def last_period() -> int:
    return engine.query(
        sql="SELECT DISTINCT MAX(e.período) AS MAX_PERIOD FROM espelho e",
        show_spinner=False,
        ttl=0
    )["max_period"].iloc[0]


take_year: int = int(last_period() / 100)
take_month: int = last_period() % 100


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_extract_monthly(receive_year: int, receive_month: int) -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT l.lançamento, e.período, e.acerto, e.valor
               FROM espelho e INNER JOIN lançamento l ON l.id_lançamento = e.id_lançamento
               WHERE e.período / 100 = :get_year
                 AND e.período % 100 = :get_month
               ORDER BY e.período, e.acerto DESC, e.valor DESC""",
        show_spinner=False,
        ttl=0,
        params=dict(get_year=receive_year, get_month=receive_month),
    )
    load.columns = [str(coluna).capitalize() for coluna in load.columns]
    load["Período"] = pd.to_datetime(load["Período"], format="%Y%m").dt.strftime("%B de %Y")

    return load


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_extract_annual(receive_year: int) -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT l.lançamento, e.período, e.acerto, e.valor
               FROM espelho e INNER JOIN lançamento l ON l.id_lançamento = e.id_lançamento
               WHERE e.período / 100 = :get_year""",
        show_spinner=False,
        ttl=0,
        params=dict(get_year=receive_year),
    )
    load.columns = [str(coluna).capitalize() for coluna in load.columns]
    load["Mês"] = pd.to_datetime(load["Período"], format="%Y%m").dt.strftime("%b")
    load = load.pivot(columns="Mês", index=["Lançamento", "Acerto"], values="Valor") \
        .reset_index() \
        .fillna(value=0)
    load = load.reindex(columns=["Lançamento", "Acerto"] + [month for month in sort_months if month in load.columns])
    load["Média"] = load.mean(axis=1, numeric_only=True)
    load["Total"] = load[load.columns[1:-1]].sum(axis=1)
    load = load.sort_values(by=["Acerto", "Total"], ascending=[False, False])

    return load


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_total_annual() -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT e.período, SUM(e.valor) AS valor
               FROM espelho e
               GROUP BY e.período
               ORDER BY e.período""",
        show_spinner=False,
        ttl=0,
    )
    load["Ano"] = pd.to_datetime(load["período"], format="%Y%m").dt.year
    load["Mês"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%b")
    load = load.pivot(columns="Mês", index="Ano", values="valor").fillna(0)
    load = load.reindex(columns=[month for month in sort_months if month in load.columns])
    load["Média"] = load.mean(axis=1)
    load["Total"] = load[load.columns[:-1]].sum(axis=1)

    return load


@st.dialog(title=f"Inclusão de Contracheque do Mês de {date.today():%B}", width="large")
def new_data():
    de_new = st.data_editor(
        data=pd.DataFrame(columns=["id_lançamento", "período", "acerto", "valor"]),
        use_container_width=True,
        column_config={
            "id_lançamento": st.column_config.SelectboxColumn(
                label="Index",
                width="large",
                options=get_release().values()
            ),
            "período": st.column_config.NumberColumn(label="Período", min_value=200507, max_value=203012, default=202505),
            "acerto": st.column_config.CheckboxColumn(label="Acerto"),
            "valor": st.column_config.NumberColumn(label="Valor", format="dollar"),
        },
        num_rows="dynamic",
    )

    st.button(label="**Salvar**", type="primary", icon=":material/save:")

    if de_new.empty:
        st.toast("**Preencha os dados do contracheque.**", icon=":material/warning:")

    else:
        de_new.to_sql(name="espelho", con=engine, if_exists="append", index=False)
        st.toast("**Inclusão do novo contracheque com sucesso!.**", icon=":material/check_circle:")
        time.sleep(2)
        st.rerun()


tab1, tab2, tab3, tab4 = st.tabs(["**Extrato Mensal**", "**Extrato Anual**", "**Total Anual**", "**Gráfico**"])

with tab1:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.slider(label="**Mês:**", min_value=1, max_value=12, value=take_month, key="slider_months")

        st.columns(2)[0].selectbox(
            label="**Ano:**",
            options=range(date.today().year, 2004, -1),
            index=0 if take_year == date.today().year else 1,
            key="select_year",
        )

        st.button(label="**Incluir no Contracheque**", key="insert", type="primary",
                  icon=":material/add_circle:", on_click=new_data)

    with col2:
        df1: pd.DataFrame = load_extract_monthly(st.session_state["select_year"], st.session_state["slider_months"])

        st.data_editor(
            data=df1,
            height=318,
            use_container_width=True,
            hide_index=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")},
            key="de_monthly",
            row_height=25,
        )

with tab2:
    st.slider(
        label="**Ano:**",
        min_value=2005,
        max_value=date.today().year,
        value=take_year,
        key="slider_years",
    )

    df2: pd.DataFrame = load_extract_annual(st.session_state["slider_years"])

    st.data_editor(
        data=df2,
        height=318,
        use_container_width=True,
        hide_index=True,
        column_config={key: st.column_config.NumberColumn(format="dollar")
                       for key in df2.columns if key not in ["Lançamento", "Acerto"]},
        key="de_annual",
        row_height=25,
    )

with tab3:
    df3: pd.DataFrame = load_total_annual()

    with st.container():
        st.data_editor(
            data=df3,
            use_container_width=True,
            column_config={key: st.column_config.NumberColumn(format="dollar") for key in df3.columns},
            key="de_total_annual",
            row_height=25,
        )

with tab4:
    st.slider(
        label="**Ano:**",
        min_value=2005,
        max_value=date.today().year,
        value=take_year,
        key="slider_graphic",
    )

    df4: pd.DataFrame = load_total_annual()
    df4 = df4[df4.columns[:-2]]

    fig, ax = plt.subplots(figsize=(16, 6))
    plt.style.use("ggplot")

    axe = sns.barplot(data=df4.loc[st.session_state["slider_graphic"]])
    ax.set_title(label=f"Espelho - {st.session_state["slider_graphic"]}", loc="center", fontweight="bold", fontsize=12)
    ax.set(xlabel="", ylabel="", yticks=[])

    for container in ax.containers:
        if isinstance(container, BarContainer):
            ax.bar_label(
                container=container,
                fmt=lambda i: locale.currency(val=i, symbol=False, grouping=True),
                fontweight="bold",
                fontsize=10,
            )

    st.pyplot(plt, use_container_width=True)
