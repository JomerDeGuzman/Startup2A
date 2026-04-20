import streamlit as st

from logic import pending_tasks, spent_total, today_plan
from store import load_data
from ui import render_sidebar
from session_manager import validate_session, cleanup_expired_sessions

st.set_page_config(page_title='Student Quest', layout='wide')

# Cleanup expired sessions
cleanup_expired_sessions()

# Restore session from URL params if needed
query_params = st.query_params
if "session_id" in query_params:
    session_id = query_params["session_id"]
    username = validate_session(session_id)
    if username:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.session_id = session_id

# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("Login.py")
    st.stop()

# Once logged in, ensure URL always has session_id for persistence across reloads
if st.session_state.get("session_id"):
    session_id = st.session_state.session_id
    if "session_id" not in query_params:
        st.query_params["session_id"] = session_id

st.header("Hello student, survive this semester!")
username = st.session_state.get("username")
data = load_data(username)
render_sidebar(data,active_page='Home')
pending = pending_tasks(data)
spending = spent_total(data)
budget = float(data.get('daily_budget', 0) or 0)
left = budget - spending
done_count = len(data['tasks']) - len(pending)
budget_percent = min(100, int((spending / budget) * 100)) if budget > 0 else 0

st.markdown(
    """
    <style>
    :root {
            --home-card-bg: var(--secondary-background-color);
            --home-card-text: var(--text-color);
            --home-card-note-bg: var(--secondary-color);
            --home-note-text: var(--text-color);
            --home-profile-title: #f59e0b;
            --home-profile-border: #f59e0b;
            --home-quest-border: #8b5cf6;
            --home-quest-title: #8b5cf6;
            --home-tomorrow-border: #0ea5e9;
            --home-tomorrow-title: #0ea5e9;
            --home-mood-border: #ef4444;
                
                }
        .home-info-card {
            min-height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            background-color: #1e1e1e !important;
            color: #ffffff !important;
            padding: 20px !important;
            border-radius: 10px !important;
        }

        .home-info-card h3 {
            margin-top: 0 !important;
            margin-bottom: 10px !important;
        }

        .home-info-card p {
            margin: 5px 0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    col1.metric("Pending Tasks", len(pending), delta= "to do")
with col2:
    col2.metric("Completed Tasks", done_count, delta= "done")
with col3:
    col3.metric("Spend Today", f"{spending:.2f}", delta="none")
with col4:
    col4.metric("Budget Left", f"{left:.2f}", delta=f"{budget_percent}% used")

st.divider()

info_col1, info_col2, info_col3 = st.columns([2, 1, 1])

with info_col1:
    st.markdown("""
    <div class="home-info-card" style="border-left: 4px solid #f59e0b;">
    <h3 style="color: #f59e0b; margin-top: 0;">Profile</h3>
    <p style="color: #ffffff;"><strong>{}</strong></p>
    <p style="color: #ffffff;">Mood: <span style="font-weight: bold; color: #f59e0b;">{}</span></p>
    </div>
    """.format(data['student_name'], data['mood']), unsafe_allow_html=True)

with info_col2:
    st.markdown(f"""
    <div class="home-info-card" style="border-left: 4px solid #8b5cf6;">
    <h3 style="color: #8b5cf6; margin-top: 0;">Today's Plan</h3>
    <p style="color: #ffffff;">Coins : <strong style="font-size: 1.3em; color: #f59e0b;">{data['coins']}</strong></p>
    <p style="color: #ffffff;">Level : <strong style="font-size: 1.3em; color: #f59e0b;">{data['level']}</strong></p>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    tomorrow_text = data.get("tomorrow_needs") or "No preparations notes yet."
    st.markdown(f"""
    <div class="home-info-card" style="border-left: 4px solid #0ea5e9;">
    <h3 style="color: #0ea5e9; margin-top: 0;">Tomorrow's Needs</h3>
    <p style="color: #ffffff;">{tomorrow_text}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.header("Today's Plan")
plan = today_plan(data)
if plan:
    for i, item in enumerate(plan, 1):
        st.markdown(f"**{i}. {item}**")
    else:
        st.markdown("There are no tasks scheduled for today. Enjoy your leisure time or add some activities to your schedule!")

st.divider()
                                        
                                         