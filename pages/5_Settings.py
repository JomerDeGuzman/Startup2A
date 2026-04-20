import streamlit as st

from store import default_data, load_data, save_data
from ui import render_sidebar
st.set_page_config(page_title='Settings', layout='wide')

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")
    st.stop()

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
    Use this to clear your data and start fresh. This will reset your name, mood, tasks, expenses, coins, level, and daily budget to their default values.
    </p>
    </div>
    """,unsafe_allow_html=True)

st.write("")


if st.button("Reset Data", use_container_width=False):
    save_data(default_data(), username)
    st.success("Data reset successfully!")
    st.rerun()