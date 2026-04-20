import streamlit as st

from store import default_data, load_data, save_data
from ui import render_sidebar

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first!")
    st.stop()