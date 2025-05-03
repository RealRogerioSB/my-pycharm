import time

import pandas as pd
import streamlit as st
from sqlalchemy import text
from streamlit.connections import SQLConnection

st.cache_data.clear()

engine: SQLConnection = st.connection(name="AIVEN-PG", type=SQLConnection)


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_course() -> pd.DataFrame:
    return engine.query(sql="SELECT id_curso, nm_curso, hr_curso FROM unibb", show_spinner=False, ttl=0)


@st.dialog(title="Adicionar Curso")
def add_course():
    col1, col2 = st.columns(2)
    col1.number_input("Código do Curso", min_value=1, max_value=999999, key="new_id_curso")
    col2.number_input("Carga Horária", min_value=1, max_value=100, key="new_hr_curso")
    st.text_input("Nome do Curso", placeholder="Nome do Curso", key="new_nm_curso")
    st.button("**Incluir**", key="btn_add", type="primary", icon=":material/add_circle:")

    if st.session_state["btn_add"]:
        with engine.session as session:
            session.execute(
                statement=text("INSERT INTO unibb (id_curso, nm_curso, hr_curso) VALUES (:id, :nm, :hr)"),
                params=dict(
                    id=st.session_state["new_id_curso"],
                    nm=st.session_state["new_nm_curso"],
                    hr=st.session_state["new_hr_curso"]
                )
            )
            session.commit()
            st.toast("**Curso adicionado com sucesso!**", icon=":material/check_circle:")
            st.session_state["course"] = load_course().copy()
            time.sleep(1)
        st.rerun()


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_duplicity() -> pd.DataFrame:
    return engine.query(
        sql="""SELECT id_curso, nm_curso, hr_curso
               FROM unibb
               WHERE nm_curso IN (SELECT nm_curso FROM unibb GROUP BY nm_curso HAVING COUNT(nm_curso) > 1)
               ORDER BY nm_curso, id_curso""",
        show_spinner=False,
        ttl=0,
    )


if "course" not in st.session_state:
    st.session_state["course"] = load_course()

tab1, tab2 = st.tabs(["**Cursos da UniBB**", "**Cursos Duplicados**"])

with tab1:
    st.data_editor(
        data=st.session_state["course"],
        hide_index=True,
        column_config={
            "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
            "hr_curso": st.column_config.NumberColumn(label="Horas", width="small"),
        },
        key="de_course",
        row_height=25,
    )

    st.button("**Adicionar**", key="add_course", type="primary", icon=":material/add_circle:", on_click=add_course)

with tab2:
    st.data_editor(
        data=load_duplicity(),
        hide_index=True,
        column_config={
            "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
            "hr_curso": st.column_config.NumberColumn(label="Horas", width="small"),
        },
        key="de_duplicity",
        row_height=25,
    )
