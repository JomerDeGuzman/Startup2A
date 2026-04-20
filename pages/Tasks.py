import streamlit as st

from logic import make_id, refresh_level, task_reward
from store import load_data, save_data
from ui import render_sidebar

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("Please login first!")
    st.stop()
    
st.set_page_config(page_title='Student Quest - Settings', layout='wide')

st.title("Tasks")

data = load_data()
render_sidebar(data, active_page='Tasks')

with st.form("task_form", border=True):
    st.markdown("### Add New Quest")
    col1, col2 = st.columns({2, 1})

    with col1:
        title =st.text_input("Task Title", placeholder="e.g. What do you need to accomplish today?", max_chars=100)
        description = st.text_area("Task Description", placeholder="e.g. Finish math homework and review for the quiz.", max_chars=300)

    with col2:
        priority = st.selectbox("Priority", options=["Low", "Medium", "High"], index=1)

    deadline = st.date_input("Deadline (Optional)", value=None)
    add_task = st.form_submit_button("Add Quest", use_container_width=True)


# for adding task 

if add_task:
    if title.strip():
        new_task = {
            "id": make_id(),
            "title": title.strip(),
            "description": description.strip(),
            "deadline": deadline.strftime("%Y-%m-%d") if deadline else "",
            "priority": priority,
            "done": False,
        }
        save_data(data)
        st.success("Quest added successfully!")
        st.rerun()
    else:
        st.error("Please enter a title for the quest.")

st.divider()

with st.expander("Quest Rewards", expanded=False):
    reward_cols= st.columns(3)
    with reward_cols[0]:
        st.markdown("""
        <div style="background-color: #fadbd8; padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c;">
        <h4 style="color #c0392b; margin 0;">High Priority</h4>
        <p style="font-size: 1.5em; font-weight: bold; color; #e74c3c; margin: 10px 0 0 0;">8 Coins</p>
        </div>
        """, unsafe_allow_html=True)

    with reward_cols[1]:
        st.markdown("""
        <div style="background-color: #fcf3cf; padding: 15px; border-radius: 8px; border-left: 4px solid #f1c40f;">
        <h4 style="color #d4ac0d; margin 0;">Medium Priority</h4>
        <p style="font-size: 1.5em; font-weight: bold; color; #f39c12; margin: 10px 0 0 0;">5 Coins</p>
        </div>
        """, unsafe_allow_html=True)

    with reward_cols[2]:
        st.markdown("""
        <div style="background-color: #d5f5e3; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60;">
        <h4 style="color #27ae60; margin 0;">Low Priority</h4>
        <p style="font-size: 1.5em; font-weight: bold; color; #2ecc71; margin: 10px 0 0 0;">3 Coins</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

st.markdown("active quests")

if not data("tasks"):
    st.info("No quests added yet. your all set")
else:
    pending_tasks = [t for t in data["tasks"] if not t.get("done")]
    completed_tasks = [t for t in data["tasks"] if t.get("done")]

    if pending_tasks:
        st.markdown("### Pending Quests")
        for task in pending_tasks:
            priority = task["priority"]
            priority_color = {
                "High": "#e74c3c",
                "Medium": "#f39c12",
                "Low": "#2ecc71"
            }.get(priority, "#bdc3c7")
            priority_emoji = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}.get(priority, "⚪")
            reward = task_reward(priority)
            
            with st.container(border=True):
                st.markdown(f"### {task['title']} ")
                
                with col_title:
                    st.markdown(f"### {task['title']} ")
                    
                        



