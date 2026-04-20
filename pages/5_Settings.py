import streamlit as st

from store import default_data, load_data, save_data
from ui import render_sidebar
from session_manager import (
    cleanup_expired_sessions,
    create_public_session_token,
    parse_public_session_token,
    validate_session,
)

st.set_page_config(page_title='Settings', layout='wide')

# Cleanup expired sessions
cleanup_expired_sessions()

# Restore session from URL params if needed
query_params = st.query_params
if "auth" in query_params:
    session_id = parse_public_session_token(query_params["auth"])
    username = validate_session(session_id)
    if username:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.session_id = session_id

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")
    st.stop()

# Once logged in, ensure URL always has session_id for persistence across reloads
if st.session_state.get("session_id"):
    session_id = st.session_state.session_id
    auth_token = create_public_session_token(session_id)
    if query_params.get("auth") != auth_token:
        st.query_params["auth"] = auth_token

username = st.session_state.get("username")
data = load_data(username)
render_sidebar(data, active_page='Settings')

st.markdown("""
        <style>
         :root {
                --settings-page-bg: var(--text-color);
                --settings-muted-text: var(--text-color);
                --settings-card-bg: var(--secondary-color);
                --settings-card-border: var(--border-color);
            
        .settings-card {
            background-color: var(--settings-card-bg);
            padding: 1.1rem 1.25rem;
            border-radius: 0.9rem;
            border: 1px solid var(--settings-card-border);
            color: var(--settings-page-text);


        .settings-card h3,
        .settings-card p {color: inherit;}
            
        </style>
               
    """,unsafe_allow_html=True)

st.title("Settings")

st.markdown(
    """
    <div class="settings-card">
    <h3 style="margin-top: 0;">Reset Progress</h3>
    <p style="margin-bottom: 0; color: var(--settings-muted-text);">
    (Optional) Use this to clear your data and start fresh. This will reset your name, mood, tasks, expenses, coins, level, and daily budget to their default values.
    </p>
    </div>
    """,unsafe_allow_html=True)

st.write("")


if st.button("Reset Data", use_container_width=False):
    save_data(default_data(), username)
    st.success("Data reset successfully!")
    st.rerun()