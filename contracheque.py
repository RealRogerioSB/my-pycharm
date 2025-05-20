import locale
from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import text
from streamlit.connections import SQLConnection

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)

sort_months: list[str] = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def get_release() -> dict[str: int]:
    load = engine.query(
        sql="SELECT id_lançamento, lançamento FROM lançamento ORDER BY lançamento",
        show_spinner=False,
        ttl=0
    )

    return {value: key for key, value in zip(load["id_lançamento"].to_list(), load["lançamento"].to_list())}


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def last_period() -> int:
    return engine.query(
        sql="SELECT DISTINCT MAX(período) AS MAX_PERIOD FROM contracheque",
        show_spinner=False,
        ttl=0
    )["max_period"].iloc[0]


take_year: int = int(last_period() / 100)
take_month: int = last_period() % 100


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_extract_monthly(receive_year: int, receive_month: int) -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT l.lançamento, c.período, c.acerto, c.valor
               FROM contracheque c INNER JOIN lançamento l ON l.id_lançamento = c.id_lançamento
               WHERE c.período / 100 = :get_year
                 AND c.período % 100 = :get_month
               ORDER BY c.período, c.acerto DESC, c.valor DESC""",
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
        sql="""SELECT l.lançamento, c.período, c.acerto, c.valor
               FROM contracheque c INNER JOIN lançamento l ON l.id_lançamento = c.id_lançamento
               WHERE c.período / 100 = :get_year""",
        show_spinner=False,
        ttl=0,
        params=dict(get_year=receive_year),
    )
    load.columns = [str(coluna).capitalize() for coluna in load.columns]
    load["Mês"] = pd.to_datetime(load["Período"], format="%Y%m").dt.strftime("%b")
    load = load.pivot(columns="Mês", index=["Lançamento", "Acerto"], values="Valor").reset_index().fillna(value=0)
    load = load.reindex(columns=["Lançamento", "Acerto"] + [month for month in sort_months if month in load.columns])
    load["Média"] = load[load.columns[2:]].mean(axis=1)
    load["Total"] = load[load.columns[2:-1]].sum(axis=1)
    load = load.sort_values(by=["Acerto", "Total"], ascending=[False, False])

    return load


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_total_annual() -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT período, SUM(valor) AS valor
               FROM contracheque
               GROUP BY período
               ORDER BY período""",
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


@st.dialog(title=f"Inclusão do Mês de {date.today():%B}", width="large")
def new_data() -> None:
    message = st.empty()

    get = get_release()

    st.data_editor(
        data=pd.DataFrame(columns=["id_lançamento", "período", "acerto", "valor"]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "id_lançamento": st.column_config.SelectboxColumn(
                label="Lançamento",
                width="large",
                required=True,
                options=get.keys(),
            ),
            "período": st.column_config.NumberColumn(
                label="Período",
                default=date.today().year * 100 + date.today().month,
                min_value=200001,
                max_value=203012,
                required=True,
            ),
            "acerto": st.column_config.CheckboxColumn(
                label="Acerto",
                required=True,
                default=False
            ),
            "valor": st.column_config.NumberColumn(
                label="Valor",
                required=True,
                default=0.0,
                format="dollar"
            ),
        },
        key="editor",
        num_rows="dynamic",
    )

    st.button("Salvar", key="save", type="primary", icon=":material/save:")

    if st.session_state["save"]:
        if not st.session_state["editor"]["added_rows"]:
            message.warning("**A planilha não foi alterada...**", icon=":material/warning:")
            st.stop()

        for row in st.session_state["editor"]["added_rows"]:
            row["id_lançamento"] = get.get(row["id_lançamento"])

        with engine.session as session:
            for row in st.session_state["editor"]["added_rows"]:
                session.execute(
                    statement=text("INSERT INTO contracheque (id_lançamento, período, acerto, valor) "
                                   "VALUES (:id_lançamento, :período, :acerto, :valor)"),
                    params=dict(
                        id_lançamento=row["id_lançamento"],
                        período=row["período"],
                        acerto=row["acerto"],
                        valor=row["valor"],
                    ),
                )

            session.commit()

        message.info("**Inclusão do novo registro com sucesso!**", icon=":material/check_circle:")

        st.cache_data.clear()

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
        st.data_editor(
            data=load_extract_monthly(st.session_state["select_year"], st.session_state["slider_months"]),
            use_container_width=True,
            hide_index=True,
            column_config={"Valor": st.column_config.NumberColumn(format="dollar")},
            key="de_monthly",
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
        use_container_width=True,
        hide_index=True,
        column_config={key: st.column_config.NumberColumn(format="dollar")
                       for key in df2.columns if key not in ["Lançamento", "Acerto"]},
        key="de_annual",
    )

with tab3:
    df3: pd.DataFrame = load_total_annual()

    with st.container():
        st.data_editor(
            data=df3,
            use_container_width=True,
            column_config={key: st.column_config.NumberColumn(format="dollar") for key in df3.columns},
            key="de_total_annual",
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
    df4 = df4[df4.columns[:-2]] \
        .loc[st.session_state["slider_graphic"]] \
        .reset_index() \
        .rename(columns={st.session_state["slider_graphic"]: "salário"})

    fig = px.bar(
        data_frame=df4,
        x="Mês",
        y="salário",
        title=f"Espelho {st.session_state["slider_graphic"]}",
        text=df4["salário"].apply(lambda x: locale.currency(x, grouping=True)),
        color="salário",
        color_continuous_scale="Viridis"
    )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        xaxis=dict(
            showline=True,
            linewidth=1,
            linecolor="gray",
            showgrid=True
        ),
        yaxis=dict(showticklabels=False),
        showlegend=False,
        coloraxis_showscale=True,
        template="presentation",
        margin=dict(l=0, r=0, t=30, b=0),
        font=dict(size=13, color="black"),
    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)
