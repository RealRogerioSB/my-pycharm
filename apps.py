import streamlit as st

st.set_page_config(
    page_title="Meus Apps",
    layout="wide",
)

st.markdown(
    body="""<style>
        [data-testid='stHeader'] {display: none;}
        #MainMenu {visibility: hidden} footer {visibility: hidden}
    </style>""",
    unsafe_allow_html=True
)

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
