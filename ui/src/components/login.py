import streamlit as st
from client.ontobridge import OntobridgeClient
from model.user import User


def handle_login_state(access_token: str):
    st.session_state.access_token = access_token
    st.session_state.is_authenticated = True
    me = get_me()
    st.session_state.user = User(
        username = me.username,
        active = me.active,
        role = me.role,
    )

def handle_logout_state():
    st.session_state.is_authenticated = False
    st.session_state.access_token = None
    st.session_state.user = None

def get_me() -> User:
    ontobridge_client = OntobridgeClient()
    response = ontobridge_client.get_me()
    
    return User(**response.json())

def handle_login(username: str, password: str):
    ontobridge_client = OntobridgeClient()
    response = ontobridge_client.login(username, password)
    if response.status_code == 200:
        st.success(f"Logged in as {username}")
        access_token = response.json()["access_token"]
        handle_login_state(access_token)
        # set_access_token_cookie(access_token)
        st.rerun()
    else:
        st.error(response.reason)

def handle_logout():
    handle_logout_state()
    st.rerun()

def login_form():
    left_col, middle_col, right_col = st.columns([5,7,5])
    middle_col.markdown("### Onto-Terminology AI Translator :material/graph_5:")
    with middle_col.form("login_form"):
        st.markdown("### Login")
        username = st.text_input("Username", key="login_form_username")
        password = st.text_input("Password", type="password", key="login_form_password")
        submit = st.form_submit_button("Log In")
        if submit:
            if username and password:
                handle_login(username, password)
            else:
                st.error("Please enter username and password.")

def login():
    login_form()
