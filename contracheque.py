import locale
from datetime import date

import pandas as pd
import plotly.express as px
from sqlalchemy import text
import streamlit as st
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
    load["Média"] = load.mean(axis=1, numeric_only=True)
    load["Total"] = load[load.columns[1:-1]].sum(axis=1)
    load = load.sort_values(by=["Acerto", "Total"], ascending=[False, False])

    return load


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_total_annual() -> pd.DataFrame:
    load: pd.DataFrame = engine.query(
        sql="""SELECT c.período, SUM(c.valor) AS valor
               FROM contracheque c
               GROUP BY c.período
               ORDER BY c.período""",
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
            message.warning("**Preencha os dados do registro.**", icon=":material/warning:")
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

    df4: pd.DataFrame = load_total_annual().drop(["Média", "Total"], axis=1) \
        .loc[st.session_state["slider_graphic"]].reset_index()
    df4 = df4.rename(columns={st.session_state["slider_graphic"]: "salário"})
    df4["salário"] = df4["salário"].apply(lambda val: locale.format_string("%.2f", val, grouping=True))

    fig = px.bar(
        data_frame=df4,  # define o DataFrame como fonte de dados para o gráfico
        x="Mês",  # define os meses como eixo X
        y="salário",  # define os salários como eixo Y
        title=f"Espelho {st.session_state["slider_graphic"]}",  # define o título do gráfico
        text=df4["salário"],  # exibe os valores salariais formatados no padrão brasileiro sobre as barras
        color="salário",  # define a cor das barras com base nos valores salariais
        color_continuous_scale="Viridis"  # aplica um esquema de cor gradiente ao gráfico
    )

    # ajusta elementos visuais do layout do gráfico
    fig.update_layout(
        xaxis_title="",  # remove o título do eixo X
        yaxis_title="",  # remove o título do eixo Y
        xaxis=dict(
            showline=True,  # adiciona uma linha no eixo X abaixo dos meses
            linewidth=1,  # define a espessura da linha do eixo X
            linecolor="gray",  # define a cor da linha do eixo X
            showgrid=True  # exibe uma grade de fundo para facilitar a leitura dos valores
        ),
        yaxis=dict(showticklabels=False),  # exibe os marcadores de valor no eixo Y
        showlegend=False,  # remove a legenda do gráfico
        coloraxis_showscale=True,  # exibe a escala de cores ao lado do gráfico
        template="presentation",  # aplica um tema mais profissional ao gráfico
        margin=dict(l=0, r=0, t=30, b=0),  # define as margens do gráfico
        font=dict(size=13, color="black"),  # define o tamanho e a cor da fonte utilizada
    )

    fig.update_traces(textposition="outside")  # posiciona os valores acima de cada barra para melhor legibilidade

    st.plotly_chart(fig, use_container_width=True)
