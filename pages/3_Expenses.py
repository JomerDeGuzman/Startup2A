import streamlit as st

from logic import add_history_entry, make_id
from store import load_data, save_data
from ui import render_sidebar
from session_manager import (
    cleanup_expired_sessions,
    create_public_session_token,
    parse_public_session_token,
    validate_session,
)

st.set_page_config(page_title='Expenses - Student Quest', layout='wide')

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

st.title("Expenses")

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
        expense = {
            "id": make_id(),
            "label": label.strip(),
            "amount": float(amount),
        }
        data["expenses"].append(expense)
        add_history_entry(data, "expense", "add", title=expense["label"], amount=expense["amount"], expense_id=expense["id"])
        save_data(data, username)
        st.success(f"Expense added! {amount:.2f}")
        st.rerun()
    else:
        st.error("Please enter a valid description and amount greater than 0.")

st.divider()

st.markdown("### Today's Expenses")

if not data["expenses"]:
    st.info("No expenses added yet. Use the form above to add your first expense.")
else:
    for i, expense in enumerate (data["expenses"], 1):
        amount = float(expense['amount'])

        with st.container(border=True):
            col_main, col_amount, col_actions = st.columns([2,1,1])

            with col_main:
                st.markdown(f"**{i}. {expense['label']}**")
            
            with col_amount:
                st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color: #e74c3c;'>₱{amount:.2f}</p>", unsafe_allow_html=True)

            with col_actions:
                if st.button("Remove", key=f"expense_{expense['id']}", use_container_width=True):
                    add_history_entry(data, "expense", "remove", title=expense["label"], amount=amount, expense_id=expense["id"])
                    data["expenses"] = [item for item in data["expenses"] if item["id"] != expense["id"]]
                    save_data(data, username)
                    st.success("Expense removed!")
                    st.rerun()

st.divider()

st.markdown("### Expense History")
expense_history = [item for item in data.get("history", []) if item.get("category") == "expense"]
if not expense_history:
    st.info("No expense history yet.")
else:
    for entry in expense_history[:10]:
        title_text = entry.get("title", "Expense")
        action = entry.get("action", "updated").replace("_", " ").title()
        amount_text = f" - ₱{float(entry.get('amount', 0)):.2f}" if entry.get("amount") is not None else ""
        st.write(f"{entry.get('timestamp', '')} - {action}: {title_text}{amount_text}")




        
