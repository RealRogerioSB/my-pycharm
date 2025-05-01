import time

import pandas as pd
import streamlit as st
from sqlalchemy import text
from streamlit.connections import SQLConnection

st.header(":material/book_5: Cursos da UniBB")

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_unibb() -> pd.DataFrame:
    return engine.query(sql="SELECT * FROM unibb", show_spinner=False, ttl=0)


@st.dialog(title="Adicionar Curso")
def add_unibb():
    col1, col2 = st.columns(2)
    col1.number_input("Código do Curso", min_value=1, max_value=999999, key="new_id_curso")
    col2.number_input("Carga Horária", min_value=1, max_value=100, key="new_hr_curso")
    st.text_input("Nome do Curso", placeholder="Nome do Curso", key="new_nm_curso")
    st.button("**Incluir**", key="btn_add", type="primary", icon=":material/add_circle:")

    if st.session_state["btn_add"]:
        with engine.session as session:
            session.execute(
                text("INSERT INTO unibb (id_curso, nm_curso, hr_curso) VALUES (:id, :nm, :hr)"),
                dict(
                    id=st.session_state["new_id_curso"],
                    nm=st.session_state["new_nm_curso"],
                    hr=st.session_state["new_hr_curso"]
                )
            )
            session.commit()
            st.success("**Curso adicionado com sucesso!**", icon=":material/check_circle:")
            time.sleep(1)
        st.rerun()


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_duplicity() -> pd.DataFrame:
    return engine.query(
        sql="""SELECT *
               FROM unibb
               WHERE nm_curso IN (SELECT nm_curso FROM unibb GROUP BY nm_curso HAVING COUNT(nm_curso) > 1)
               ORDER BY nm_curso, id_curso""",
        show_spinner=False
    )


tab1, tab2 = st.tabs(["**Cursos da UniBB**", "**Cursos Duplicados**"])

with tab1:
    st.data_editor(
        data=load_unibb(),
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn(label="Index", width="small"),
            "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
            "hr_curso": st.column_config.NumberColumn(label="Horas", width="small"),
        },
        key="de_unibb",
        row_height=25,
    )

    st.button("**Adicionar**", key="add_unibb", type="primary", icon=":material/add_circle:", on_click=add_unibb)

with tab2:
    st.data_editor(
        data=load_duplicity(),
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn(label="Index", width="small"),
            "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
            "hr_curso": st.column_config.NumberColumn(label="Horas", width="small"),
        },
        key="de_duplicity",
        row_height=25,
    )
