import os
import streamlit as st

st.set_page_config(page_title="Teste...", page_icon=":material/home:", layout="wide")

st.page_link(os.path.join(os.getcwd(), "pages", "1_config.py"), label="Configuração", icon=":material/settings:")
st.page_link(os.path.join(os.getcwd(), "pages", "2_tool.py"), label="Ferramenta", icon=":material/construction:")
st.page_link(os.path.join(os.getcwd(), "pages", "3_help.py"), label="Ajuda", icon=":material/help:")
