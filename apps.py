import streamlit as st

if "toggle_sidebar" not in st.session_state:
    st.session_state["toggle_sidebar"] = "expanded"

st.set_page_config(
    page_title="Meus Apps",
    layout="wide",
    page_icon="🇧🇷",
    initial_sidebar_state=st.session_state["toggle_sidebar"],
)


def toggle_sidebar() -> None:
    if st.session_state["toggle_sidebar"] == "expanded":
        st.session_state["toggle_sidebar"] = "collapsed"
    else:
        st.session_state["toggle_sidebar"] = "expanded"


with open("styles/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.header(":material/home: Menu")

    st.markdown("")

    if st.button("**Contracheque**", key="btn1", type="tertiary", icon=":material/payments:",
                 use_container_width=True, on_click=toggle_sidebar):
        st.switch_page("pages/contracheque.py")

    if st.button("**Mega-Sena**", key="btn2", type="tertiary", icon=":material/nest_thermostat_e_eu:",
                 use_container_width=True, on_click=toggle_sidebar):
        st.switch_page("pages/megasena.py")

    if st.button("**Cursos da UniBB**", key="btn3", type="tertiary", icon=":material/auto_stories:",
                 use_container_width=True, on_click=toggle_sidebar):
        st.switch_page("pages/unibb.py")

st.title(":material/logo_dev: Meus Apps")
