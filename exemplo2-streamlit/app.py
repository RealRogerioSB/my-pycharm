import os
import streamlit as st

if "sidebar_state" not in st.session_state:
    st.session_state["sidebar_state"] = "expanded"

st.set_page_config(
    page_title="Teste...",
    page_icon=":material/house:",
    layout="wide",
    initial_sidebar_state=st.session_state["sidebar_state"],
    menu_items={
        "Get help": "https://www.bb.com.br",
        "Report a bug": "mailto:rogerioballoussier@bb.com.br",
        "About": "Desenvolvimento e elaboração pelo **GEFID** em 22/04/2025"},
)

st.title("Teste de Streamlit")


def tooggle_sidebar():
    if st.session_state["sidebar_state"] == "expanded":
        st.session_state["sidebar_state"] = "collapsed"
    else:
        st.session_state["sidebar_state"] = "expanded"


with st.sidebar:
    st.header(":material/house: Menu")

    with st.expander("**1. Página**"):
        if st.button("**Configuração**", icon=":material/settings:", on_click=tooggle_sidebar, use_container_width=True):
            st.switch_page(os.path.join(os.getcwd(), "pages", "1_config.py"))

    with st.expander("**2. Página**"):
        if st.button("**Ferramenta**", icon=":material/construction:", on_click=tooggle_sidebar, use_container_width=True):
            st.switch_page(os.path.join(os.getcwd(), "pages", "2_tool.py"))

    with st.expander("**3. Página**"):
        if st.button("**Ajuda**", icon=":material/help:", on_click=tooggle_sidebar, use_container_width=True):
            st.switch_page(os.path.join(os.getcwd(), "pages", "3_help.py"))
