# CREATE TABLE IF NOT EXISTS unibb (
#     id SERIAL PRIMARY KEY,
#     id_curso INTEGER NOT NULL,
#     nm_curso VARCHAR(100) NOT NULL,
#     hr_curso INTEGER NOT NULL
# )

import pandas as pd
import streamlit as st
from streamlit.connections import SQLConnection

st.set_page_config(page_title="Cursos da UniBB")

engine = st.connection(name="AIVEN-PG", type=SQLConnection)

if "offset" not in st.session_state:
    st.session_state["offset"] = 0


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_unibb() -> pd.DataFrame:
    return engine.query(
        sql="""
            SELECT id_curso, nm_curso, hr_curso
            FROM unibb
            ORDER BY id_curso
        """,
        show_spinner=False
    )


def rows_page(df: pd.DataFrame, offset: int) -> pd.DataFrame:
    return df.iloc[offset:offset + 10]


unibb = load_unibb()

col = st.columns([4.5, 0.2, 1.475, 0.025])

with col[0]:
    st.markdown("#### Lista de Cursos da UniBB")

with col[2]:
    side = st.columns(4)

    with side[0]:
        if st.button("⏮"):
            st.session_state["offset"] = 0
            rows_page(unibb, st.session_state["offset"])
            st.rerun()

    with side[1]:
        if st.button("️◀"):
            st.session_state["offset"] = max(0, st.session_state["offset"] - 10)
            rows_page(unibb, st.session_state["offset"])
            st.rerun()

    with side[2]:
        if st.button("▶"):
            st.session_state["offset"] = min(len(unibb) - 10, st.session_state["offset"] + 10)
            rows_page(unibb, st.session_state["offset"])
            st.rerun()

    with side[3]:
        if st.button("⏭"):
            st.session_state["offset"] = len(unibb) - 10
            rows_page(unibb, st.session_state["offset"])
            st.rerun()

st.data_editor(
    data=rows_page(unibb, st.session_state["offset"]),
    hide_index=True,
    height=313,
    column_config={
        "id_curso": st.column_config.NumberColumn(label="Código", required=True, width="small", default=100000),
        "nm_curso": st.column_config.TextColumn(label="Curso", required=True, width="large", default="nome-curso"),
        "hr_curso": st.column_config.NumberColumn(label="Horas", required=True, width="small", default=0),
    },
    key="default",
    num_rows="dynamic",
    row_height=25,
)

if st.session_state.default.get('added_rows', 0):
    st.markdown("**Adição detectada:**")
    st.json(st.session_state["default"]["added_rows"])

if st.session_state.default.get('edited_rows', 0):
    st.markdown("**Edição detectada:**")
    st.json(st.session_state["default"]["edited_rows"])

if st.session_state.default.get('deleted_rows', 0):
    st.markdown("**Remoção detectada:**")
    st.json(st.session_state["default"]["deleted_rows"])


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_duplicity() -> pd.DataFrame:
    return engine.query(
        sql="""
            SELECT *
            FROM unibb
            WHERE nm_curso IN (SELECT nm_curso FROM unibb GROUP BY nm_curso HAVING COUNT(nm_curso) > 1)
            ORDER BY nm_curso, id_curso
        """,
        show_spinner=False
    )


st.markdown("#### Lista de Cursos Duplicados")

st.data_editor(
    data=load_duplicity(),
    hide_index=True,
    height=188,
    column_config={
        "id": st.column_config.NumberColumn(label="Index", width="small"),
        "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
        "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
        "hr_curso": st.column_config.NumberColumn(label="Horas", width="small"),
    },
    key="duplo",
    row_height=25,
)
