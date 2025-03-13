import os
import streamlit as st

st.subheader("❓ Ajuda")
st.page_link(os.path.join(os.getcwd(), "app.py"), label="Voltar", icon=":material/home:")
