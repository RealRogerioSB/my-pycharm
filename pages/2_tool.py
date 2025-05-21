# esse arquivo vem juntamente com o arquivo 'app.py' que é página principal
import streamlit as st
from app import toggle_sidebar

st.header(":material/construction: Ferramenta")

if st.button("**Voltar**", type="primary", icon=":material/reply:", on_click=toggle_sidebar):
    st.switch_page("app.py")
