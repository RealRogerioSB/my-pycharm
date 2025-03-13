import os
import streamlit as st

st.subheader("🛠 Ferramenta")
st.page_link(os.path.join(os.getcwd(), "app.py"), label="Voltar", icon=":material/home:")
