import streamlit as st

from logic import spent_total
from store import load_data, save_data
from ui import render_sidebar

st.set_page_config(page_title='Expenses - Student Quest', layout='wide')

st.title("Expenses")

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Login.py")
    st.stop()

username = st.session_state.get("username")
data = load_data(username)
render_sidebar(data, active_page='Expenses')

with st.form("expenses_form", border=True):
    st.markdown("### Add New Expense")
    col1, col2 = st.columns([2,1])

    with col1:
        label = st.text_input("what did you buy?", help="Enter a description for your expense.")
    with col2:
        amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.01)
    
    add_expense = st.form_submit_button("Add Expense", use_container_width=True)

if add_expense:
    if label.strip() and amount > 0:
        data["expenses"].append({"label": label.strip(), "amount": float(amount)})