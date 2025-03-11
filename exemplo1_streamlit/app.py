import os
import streamlit as st

st.logo("home_dark.png", icon_image="chat_dark.png")

if "role" not in st.session_state:
    st.session_state["role"] = None

ROLES = [None, "Requester", "Responser", "Admin"]


def login():
    with st.form("loginform"):
        st.header("Log in")
        _role = st.selectbox("Choose your role:", ROLES)

        if st.form_submit_button("Log in", type="primary"):
            st.session_state["role"] = _role
            st.rerun()


def logout():
    st.session_state["role"] = None
    st.rerun()


role = st.session_state["role"]

account_pages = [
    st.Page(logout, title="Log out", icon=":material/logout:"),
    st.Page(os.path.join(os.getcwd(), "settings.py"),
            title="Settings", icon=":material/settings:"),
]
request_pages = [
    st.Page(os.path.join(os.getcwd(), "request", "request_1.py"),
            title="Request 1", icon=":material/help:", default=role == "Requester"),
    st.Page(os.path.join(os.getcwd(), "request", "request_2.py"),
            title="Request 2", icon=":material/bug_report:"),
]
response_pages = [
    st.Page(os.path.join(os.getcwd(), "response", "response_1.py"),
            title="Response 1", icon=":material/healing:", default=role == "Responser"),
    st.Page(os.path.join(os.getcwd(), "response", "response_2.py"),
            title="Response 2", icon=":material/handyman:"),
]
admin_pages = [
    st.Page(os.path.join(os.getcwd(), "admin", "admin_1.py"),
            title="Admin 1", icon=":material/person_add:", default=role == "Admin"),
    st.Page(os.path.join(os.getcwd(), "admin", "admin_2.py"),
            title="Admin 2", icon=":material/security:"),
]

st.title("Request Manager")

page_dict = {}

if st.session_state["role"] in ["Requester", "Admin"]:
    page_dict["Request"] = request_pages

if st.session_state["role"] in ["Responser", "Admin"]:
    page_dict["Response"] = response_pages

if st.session_state["role"] == "Admin":
    page_dict["Admin"] = admin_pages

if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
else:
    pg = st.navigation([st.Page(login)])

pg.run()
