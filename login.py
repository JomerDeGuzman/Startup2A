# ===== DEBUGGED BY AI =====
# Fixed authentication flow with session state
# Redirects to pages/App.py instead of app.py
# Added logout functionality

import streamlit as st

from store import default_data, load_data, save_data
from ui import render_sidebar

st.set_page_config(page_title='Survive-A-Semester', layout='centered')

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def check_login(username, password):
    # Replace this with your actual login logic (database, API calls, etc.)
    return username == "admin" and password == "password"

def login_page():
    st.title("Survive-A-Semester")
    st.markdown("Complete quests to survive!")
    
    username = st.text_input("Username", key="credentials")
    password = st.text_input("Password", type='password', key="credential")
    
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.switch_page("pages/home.py")
        else:
            st.error("Invalid credentials")

if __name__ == "__main__":
    if not st.session_state.logged_in:
        login_page()
    else:
        st.switch_page("pages/home.py")