import os
import streamlit as st
from exemplo2_streamlit.app import tooggle_sidebar

st.header(":material/help: Ajuda")

if st.button("**Voltar**", icon=":material/house:", on_click=tooggle_sidebar):
    st.switch_page(os.path.join(os.getcwd(), "app.py"))
