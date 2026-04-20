import streamlit as st

from logic import add_history_entry, make_id, refresh_level, task_reward
from store import load_data, save_data
from ui import render_sidebar
from session_manager import (
    cleanup_expired_sessions,
    create_public_session_token,
    parse_public_session_token,
    validate_session,
)

st.set_page_config(page_title="Tasks - Student Survival Planner", layout="wide")

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

st.title(" Tasks & Quests")

username = st.session_state.get("username")
data = load_data(username)
render_sidebar(data, active_page="Tasks")

# Add task form
with st.form("task_form", border=True):
    st.markdown("### Add New Quest")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        title = st.text_input("Task title", placeholder="What do you need to accomplish?")
        description = st.text_area("Quest description", placeholder="Add a short note about this quest", height=90)
    
    with col2:
        priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
    
    deadline = st.date_input("Deadline (optional)", value=None)
    add_task = st.form_submit_button("Add Quest", use_container_width=True)

if add_task:
    if title.strip():
        reward = task_reward(priority)
        task_id = make_id()
        data["tasks"].append(
            {
                "id": task_id,
                "title": title.strip(),
                "description": description.strip(),
                "deadline": deadline.strftime("%Y-%m-%d") if deadline else "",
                "priority": priority,
                "done": False,
            }
        )
        add_history_entry(data, "task", "add", title=title.strip(), task_id=task_id, priority=priority, reward=reward)
        save_data(data, username)
        st.success(" Quest added! Complete it to earn coins!")
        st.rerun()
    else:
        st.error("Quest title is required.")

st.divider()

# Reward information
with st.expander(" Quest Rewards", expanded=False):
    reward_cols = st.columns(3)
    with reward_cols[0]:
        st.markdown("""
        <div style="background-color: #fadbd8; padding: 15px; border-radius: 8px; border-left: 4px solid #e74c3c;">
            <h4 style="color: #c0392b; margin: 0;">High Priority</h4>
            <p style="font-size: 1.5em; font-weight: bold; color: #e74c3c; margin: 10px 0 0 0;">8 Coins</p>
        </div>
        """, unsafe_allow_html=True)
    
    with reward_cols[1]:
        st.markdown("""
        <div style="background-color: #fdebd0; padding: 15px; border-radius: 8px; border-left: 4px solid #f39c12;">
            <h4 style="color: #d68910; margin: 0;">Medium Priority</h4>
            <p style="font-size: 1.5em; font-weight: bold; color: #f39c12; margin: 10px 0 0 0;">5 Coins</p>
        </div>
        """, unsafe_allow_html=True)
    
    with reward_cols[2]:
        st.markdown("""
        <div style="background-color: #d5f4e6; padding: 15px; border-radius: 8px; border-left: 4px solid #27ae60;">
            <h4 style="color: #229954; margin: 0;">Low Priority</h4>
            <p style="font-size: 1.5em; font-weight: bold; color: #27ae60; margin: 10px 0 0 0;">2 Coins</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Task list
st.markdown("###  Active Quests")

if not data["tasks"]:
    st.info(" No quests yet! You're all set!")
else:
    # Separate pending and completed tasks
    pending_tasks = [t for t in data["tasks"] if not t.get("done")]
    completed_tasks = [t for t in data["tasks"] if t.get("done")]
    
    # Display pending tasks
    if pending_tasks:
        st.markdown("### Pending Quests")
        for task in pending_tasks:
            priority = task['priority']
            priority_color = {"High": "#e74c3c", "Medium": "#f39c12", "Low": "#27ae60"}[priority]
            priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}[priority]
            reward = int(task_reward(priority))
            
            with st.container(border=True):
                col_title, col_reward = st.columns([3, 1])
                
                with col_title:
                    st.markdown(f"### {task['title']}")
                    task_description = task.get("description", "").strip()
                    if task_description:
                        st.markdown(f"{task_description}")
                    info_cols = st.columns(3)
                    with info_cols[0]:
                        st.markdown(f"**Priority:** <span style='color: {priority_color};'>{priority_emoji} {priority}</span>", unsafe_allow_html=True)
                    with info_cols[1]:
                        st.markdown(f"**Deadline:** {task['deadline'] or 'No deadline'}")
                    with info_cols[2]:
                        st.markdown(f"**Reward:** {reward} Coins")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Finish Quest", key=f"done_{task['id']}", use_container_width=True):
                        task["done"] = True
                        data["coins"] += reward
                        refresh_level(data)
                        add_history_entry(data, "task", "complete", title=task["title"], task_id=task["id"], priority=priority, reward=reward)
                        save_data(data, username)
                        st.success(f" Quest complete! + {reward} coins!")
                        st.rerun()
                
                with col2:
                    if st.button("Delete", key=f"delete_{task['id']}", use_container_width=True):
                        add_history_entry(data, "task", "delete", title=task["title"], task_id=task["id"], priority=priority, reward=reward)
                        data["tasks"] = [item for item in data["tasks"] if item["id"] != task["id"]]
                        save_data(data, username)
                        st.rerun()
    
    # Display completed tasks
    if completed_tasks:
        st.markdown("####  Completed Quests")
        for task in completed_tasks:
            priority = task['priority']
            priority_color = {"High": "#e74c3c", "Medium": "#f39c12", "Low": "#27ae60"}[priority]
            reward = int(task_reward(priority))
            
            with st.container(border=True):
                col_title, col_reward = st.columns([3, 1])
                
                with col_title:
                    st.markdown(f"~~{task['title']}~~ **[COMPLETED]**", unsafe_allow_html=True)
                    task_description = task.get("description", "").strip()
                    if task_description:
                        st.markdown(f"{task_description}")
                    info_cols = st.columns(3)
                    with info_cols[0]:
                        st.markdown(f"**Priority:** <span style='color: {priority_color};'>{priority}</span>", unsafe_allow_html=True)
                    with info_cols[1]:
                        st.markdown(f"**Deadline:** {task['deadline'] or 'No deadline'}")
                    with info_cols[2]:
                        st.markdown(f"**Earned:** {reward} Coins")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("↩ Retake Quest", key=f"pending_{task['id']}", use_container_width=True):
                        task["done"] = False
                        refresh_level(data)
                        add_history_entry(data, "task", "reopen", title=task["title"], task_id=task["id"], priority=priority, reward=reward)
                        save_data(data, username)
                        st.success(f"Quest reset. Complete it again to earn {reward} coins!")
                        st.rerun()
                
                with col2:
                    if st.button(" Delete", key=f"delete_done_{task['id']}", use_container_width=True):
                        add_history_entry(data, "task", "delete", title=task["title"], task_id=task["id"], priority=priority, reward=reward)
                        data["tasks"] = [item for item in data["tasks"] if item["id"] != task["id"]]
                        save_data(data, username)
                        st.rerun()

st.divider()

st.markdown("### Task History")
task_history = [item for item in data.get("history", []) if item.get("category") == "task"]
if not task_history:
    st.info("No task history yet.")
else:
    for entry in task_history[:10]:
        title_text = entry.get("title", "Task")
        action = entry.get("action", "updated").replace("_", " ").title()
        reward = entry.get("reward")
        reward_text = f" - {int(reward)} coins" if reward is not None else ""
        st.write(f"{entry.get('timestamp', '')} - {action}: {title_text}{reward_text}")