# esse arquivo vem juntamente com o arquivo 'app.py' que é página principal

import streamlit as st
from app import tooggle_sidebar

st.header(":material/help: Ajuda")

if st.button("**Voltar**", icon=":material/reply:", on_click=tooggle_sidebar):
    st.switch_page("app.py")
