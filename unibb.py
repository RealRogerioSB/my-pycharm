import pandas as pd
import streamlit as st
from streamlit.connections import SQLConnection

st.set_page_config(page_title="Cursos da UniBB")

st.header("Cursos da UniBB")

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_unibb() -> pd.DataFrame:
    return engine.query(sql="SELECT * FROM unibb", show_spinner=False)


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_duplicity() -> pd.DataFrame:
    return engine.query(
        sql="""SELECT id, id_curso, nm_curso, hr_curso
               FROM unibb
               WHERE nm_curso IN (SELECT nm_curso FROM unibb GROUP BY nm_curso HAVING COUNT(nm_curso) > 1)
               ORDER BY nm_curso, id_curso""",
        show_spinner=False
    )


unibb: pd.DataFrame = load_unibb()

tab1, tab2 = st.tabs(["**Cursos da UniBB**", "**Cursos Duplicados**"])

with tab1:
    st.data_editor(
        data=unibb,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn(label="Index", required=True, width="small"),
            "id_curso": st.column_config.NumberColumn(label="Código", required=True, width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", required=True, width="large"),
            "hr_curso": st.column_config.NumberColumn(label="Horas", required=True, width="small"),
        },
        row_height=25,
    )

    if st.button("**Adicionar**", type="primary", icon=":material/add_circle:"):
        pass

with tab2:
    st.data_editor(
        data=load_duplicity(),
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn(label="Index", width="small"),
            "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
            "hr_curso": st.column_config.NumberColumn(label="Horas", width="small"),
        },
        row_height=25,
    )
