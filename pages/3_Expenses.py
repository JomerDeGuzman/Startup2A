import streamlit as st

from logic import spent_total
from store import load_data, save_data
from ui import render_sidebar

st.set_page_config(page_title='Expenses - Student Quest', layout='wide')

st.title("Expenses")

data = load_data()
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
        data["expenses"].append
    (
        {
            "id": str(len(data["expenses"]) + 1) + label.strip(),
            "label": label.strip(),
            "amount": amount,
            
        }
    )

    save_data(data)
    st.success(f"Expense added! ${amount:.2f}")
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
                st.markdown(f"<p style='font-size: 1.2rem; font-weight: bold; color; #e74c3c;'>${amount:.2f}</p>", unsafe_allow_html=True)

            with col_actions:
                if st.button("Remove", key=f"expense_{expense['id']}", use_container_width=True):
                    data["expenses"] = [item for item in data["expenses"] if item["id"] != expense["id"]]
                    save_data(data)
                    st.success("Expense removed!")
                    st.rerun()




        
