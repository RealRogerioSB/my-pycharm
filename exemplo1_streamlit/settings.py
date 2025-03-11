import streamlit as st

st.title("Settings")
st.caption(f"O estado de sessão é {st.session_state["role"]}")
