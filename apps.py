import streamlit as st

st.set_page_config(
    page_title="Meus Apps",
    layout="wide",
)

with open("styles/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.navigation(
    pages={
        "Meus Apps": [
            st.Page(page="contracheque.py", title="Meu Contracheque BB", icon=":material/payments:"),
            st.Page(page="megasena.py", title="Sorteio de Mega-Sena", icon=":material/price_check:"),
            st.Page(page="unibb.py", title="Meus Cursos UniBB", icon=":material/book_5:"),
        ],
    },
    expanded=True
).run()
