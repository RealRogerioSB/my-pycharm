import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="⏳Obtendo os dados, aguarde...")
def load_course() -> pd.DataFrame:
    return pd.read_csv("~/Documents/unibb.csv", parse_dates=["dt_curso"])


def save_csv(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.toast("**A planilha não foi alterada...**", icon=":material/error:")

    else:
        frame.to_csv("~/Documents/unibb.csv", index=False)
        st.toast("**A planilha foi alterada com sucesso!**", icon=":material/check_circle:")
        st.cache_data.clear()


tab1, tab2 = st.tabs(["**Cursos da UniBB**", "**Cursos Duplicados**"])

with tab1:
    editor = st.data_editor(
        data=load_course(),
        hide_index=True,
        column_config={
            "id_curso": st.column_config.NumberColumn(label="Código", width="small"),
            "nm_curso": st.column_config.TextColumn(label="Curso", width="large"),
            "dt_curso": st.column_config.DateColumn(label="Data", format="DD/MM/YYYY"),
            "cg_curso": st.column_config.NumberColumn(label="Horas", width="small"),
        },
        key="editor",
        num_rows="dynamic",
        row_height=25,
    )

    st.button("**Adicionar**", key="add_course", type="primary",
              icon=":material/add_circle:", on_click=save_csv, args=(editor,))
