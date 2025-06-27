from datetime import date

import pandas as pd
import streamlit as st

from apps import toggle_sidebar

file_csv: str = "~/Documents/unibb.csv"

unibb: pd.DataFrame = pd.read_csv(file_csv, parse_dates=["dt_curso"])

if "unibb" not in st.session_state:
    st.session_state["unibb"] = unibb


def save_csv(frame: pd.DataFrame) -> None:
    if unibb.equals(frame):
        st.toast("**A planilha não foi alterada...**", icon=":material/error:")

    else:
        frame["id_curso"] = frame["id_curso"].astype(int)
        frame["cg_curso"] = frame["cg_curso"].astype(int)
        frame.to_csv(file_csv, index=False)
        st.cache_data.clear()
        st.toast("**Planilha alterada com sucesso!**", icon=":material/check_circle:")


tab1, tab2 = st.tabs(["**Cursos da UniBB**", "**Cursos Duplicados**"])

with tab1:
    editor = st.data_editor(
        data=st.session_state["unibb"],
        hide_index=True,
        column_config={
            "id_curso": st.column_config.NumberColumn("Código", width="small", required=True),
            "nm_curso": st.column_config.TextColumn("Curso", width="medium", required=True),
            "dt_curso": st.column_config.DateColumn("Conclusão", format="DD/MM/YYYY", required=True,
                                                    default=date.today()),
            "cg_curso": st.column_config.NumberColumn("Horas", width="small", required=True, default=1),
            "mod_curso": st.column_config.TextColumn("Módulo", width="medium", required=True),
            "lzc_curso": st.column_config.TextColumn("Estudo", required=True),
            "cnh_curso": st.column_config.TextColumn("Conhecimento", width="medium", required=True),
            "area_cnh_curso": st.column_config.TextColumn("Área", width="medium", required=True),
        },
        num_rows="dynamic",
        row_height=25,
    )

    st.button("**Adicionar**", type="primary", icon=":material/add_circle:", on_click=save_csv, args=(editor,))

if st.button("**Voltar**", key="back", type="primary", icon=":material/reply:", on_click=toggle_sidebar):
    st.switch_page("apps.py")

with tab2:
    st.dataframe(
        data=unibb[unibb.duplicated(subset=["nm_curso"], keep=False)].sort_values(by=["nm_curso", "dt_curso"],),
        hide_index=True,
        use_container_width=True,
        column_config={
            "id_curso": st.column_config.NumberColumn("Código"),
            "nm_curso": st.column_config.TextColumn("Nome", width="medium"),
            "dt_curso": st.column_config.DateColumn("Conclusão", format="DD/MM/YYYY"),
            "cg_curso": st.column_config.NumberColumn("Carga Horária"),
            "lzc_curso": st.column_config.TextColumn("Estudo"),
            "mod_curso": st.column_config.TextColumn("Módulo", width="medium"),
            "cnh_curso": st.column_config.TextColumn("Conhecimento", width="medium"),
            "area_cnh_curso": st.column_config.TextColumn("Área", width="medium"),
        },
    )
