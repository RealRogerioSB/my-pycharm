import os
import streamlit as st

st.header(":material/settings: Configuração")

if st.button("**Voltar**", icon=":material/house:"):
    st.session_state["sidebar_state"] = "expanded"
    st.switch_page(os.path.join(os.getcwd(), "app.py"))
