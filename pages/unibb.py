from datetime import date

import pandas as pd
import streamlit as st

from apps import toggle_sidebar

unibb: pd.DataFrame = pd.read_csv("~/Documents/unibb.csv", parse_dates=["dt_curso"])

if "unibb" not in st.session_state:
    st.session_state["unibb"] = unibb


def save_csv(frame: pd.DataFrame) -> None:
    if unibb.equals(frame):
        st.toast("**A planilha não foi alterada...**", icon=":material/error:")

    else:
        frame["id_curso"] = frame["id_curso"].astype(int)
        frame["cg_curso"] = frame["cg_curso"].astype(int)
        frame.to_csv("~/Documents/unibb.csv", index=False)
        st.cache_data.clear()
        st.toast("**Planilha alterada com sucesso!**", icon=":material/check_circle:")


tab1, tab2 = st.tabs(["**Cursos da UniBB**", "**Cursos Duplicados**"])

with tab1:
    editor = st.data_editor(
        data=st.session_state["unibb"],
        hide_index=True,
        column_config={
            "id_curso": st.column_config.NumberColumn("Código", width="small", required=True),
            "nm_curso": st.column_config.TextColumn("Curso", width="large", required=True),
            "dt_curso": st.column_config.DateColumn("Data", format="DD/MM/YYYY", required=True, default=date.today()),
            "cg_curso": st.column_config.NumberColumn("Horas", width="small", required=True, default=1),
        },
        num_rows="dynamic",
        row_height=25,
    )

    st.button("**Adicionar**", type="primary", icon=":material/add_circle:", on_click=save_csv, args=(editor,))

if st.button("**Voltar**", key="back", type="primary", icon=":material/reply:", on_click=toggle_sidebar):
    st.switch_page("apps.py")
