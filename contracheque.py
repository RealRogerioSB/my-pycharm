import locale
from datetime import date

import pandas as pd
import plotly.graph_objects as go
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
    load: pd.DataFrame = engine.query(
        sql="""SELECT l.lançamento, e.período, e.acerto, e.valor
               FROM espelho e INNER JOIN lançamento l ON l.id_lançamento = e.id_lançamento
               WHERE e.período / 100 = :get_year
                 AND e.período % 100 = :get_month
               ORDER BY e.período, e.acerto DESC, e.valor DESC""",
        show_spinner=False,
        ttl=60,
        params=dict(get_year=receive_year, get_month=receive_month),
    )
    load.columns = [str(coluna).capitalize() for coluna in load.columns]
    load["Período"] = pd.to_datetime(load["Período"], format="%Y%m").dt.strftime("%B de %Y")

    return load


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
    load.columns = [str(coluna).capitalize() for coluna in load.columns]
    load["Mês"] = pd.to_datetime(load["Período"], format="%Y%m").dt.strftime("%b")
    load = load.pivot(columns="Mês", index=["Lançamento", "Acerto"], values="Valor") \
        .reset_index() \
        .fillna(value=0)[["Lançamento", "Acerto", "Jan", "Fev", "Mar", "Abr",
                          "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]]
    load["Média"] = load.mean(axis=1, numeric_only=True)
    load["Total"] = load[load.columns[1:-1]].sum(axis=1)
    load = load.sort_values(by=["Acerto", "Total"], ascending=[False, False])

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
    load["Ano"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%Y")
    load["Mês"] = pd.to_datetime(load["período"], format="%Y%m").dt.strftime("%b")
    load = load.pivot(columns="Mês", index="Ano", values="valor") \
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
        )

    with col2:
        df1: pd.DataFrame = load_extract_monthly(ano, mes)

        st.data_editor(
            data=df1,
            height=318,
            use_container_width=True,
            hide_index=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")},
            row_height=28,
        )

with tab2:
    anual: int = st.slider(
        label="**Ano:**",
        min_value=2005,
        max_value=date.today().year,
        value=take_year,
        key="slider_years",
    )

    df2: pd.DataFrame = load_extract_annual(anual)

    st.data_editor(
        data=df2,
        height=318,
        use_container_width=True,
        hide_index=True,
        column_config={key: st.column_config.NumberColumn(format="dollar")
                       for key in df2.columns if key not in ["Lançamento", "Acerto"]},
        row_height=28,
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
        key="slider_graphic",
    )

    df4: pd.DataFrame = load_graphic_annual(slider_graphic)

    # criar gráfico de barras com Plotly
    fig = go.Figure()

    # adicionar barras para cada mês
    for mes in df4.columns[1:]:
        fig.add_trace(
            go.Bar(
                x=[mes],
                y=[df4[mes].sum()],
                text=locale.currency(df4[mes].sum(), grouping=True),
                textposition="outside",
                marker=dict(color=f"rgba({hash(mes) % 255}, {hash(mes) % 200}, {hash(mes) % 150}, 0.8)"),
            )
        )

    # configurações de layout detalhadas para o tema caprichado
    fig.update_layout(
        title=f"Espelho - {slider_graphic}",
        xaxis=dict(
            showticklabels=True,
            title="",
            tickfont=dict(size=14, color="black"),
        ),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        # paper_bgcolor="linear-gradient(to bottom, rgba(0, 128, 255, 0.2), rgba(255, 255, 0, 0.1))",
        title_font=dict(size=24, color="black", family="Arial"),
        margin=dict(t=50, b=30, l=30, r=30),
        showlegend=False,
    )

    # mais refinamentos visuais
    fig.update_traces(
        marker_line_width=1.5,
        marker_line_color="rgba(0,0,0,0.7)",  # Contorno preto suave nas barras
    )

    st.plotly_chart(fig, use_container_width=True)
