import streamlit as st

from logic import pending_tasks, spent_total, today_plan
from store import load_data
from ui import render_sidebar

st.set_page_config(page_title='Student Quest', layout='wide')


data = load_data()
render_sidebar(data,active_page='Home')
pending = pending_tasks(data)
spending = spent_total(data)
left = float(data["daily_budget"]) - spending
done_count = len(data['tasks']) - len(pending)
budget_percent = min(100, int((spending / float(data["daily_budget"]) * 100))) if data["daily_budget"] > 0 else 0

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
            }

            .home-info-card .title {
                margin: 0.35rem 0;
            }
    </style>
    """
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
    <div class="home-info-card" style="background-color: var(--home-card-bg); color: var(--home-card-text); padding: 20px; border-radius: 10px; border-left: 4px solid var(--home-card-border); color: var(--home-card-text);">
    <h3 style="color: var(--home-profile-title); margin-top: 0;">Profile</h3>
    <p style="color: var(--home-card-text);"><strong>{data['student_name']}</strong></p>
    <p style="color: var(--home-card-text);">Mood: <span style="font-weight: bold; color: var(--home-mood-text);">{data['mood']}</span></p>
    </div>
    """)

with info_col2:
    st.markdown(f"""
    <div class="home-info-card" style="background-color: var(--home-card-bg); color: var(--home-card-text); padding: 20px; border-radius: 10px; border-left: 4px solid var(--home-quest-border); color: var(--home-card-text);">
    <h3 style="color: var(--home-quest-title); margin-top: 0;">Today's Plan</h3>
    <p style="color: var(--home-card-text);">Coins : <strong style="font-size: 1.3em; color: #f59e0b;">{data['coins']}</strong></p>
    <p style="color: var(--home-card-text);">Level : <strong style="font-size: 1.3em; color: var(--home-profile-title);">{data['level']}</strong></p>
    </div>
    """)

with info_col3:
    tomorrow_text = data.get("tomorrow_needs") or "No preparations notes yet."
    st.markdown(f"""
    <div class="home-info-card" style="background-color: var(--home-card-bg); color: var(--home-card-text); padding: 20px; border-radius: 10px; border-left: 4px solid var(--home-quest-border); color: var(--home-card-text);">
    <h3 style="color: var(--home-tomorrow-title); margin-top; 0;">Tomorrow's Needs</h3>
    <p style="color: var(--home-card-text);">{tomorrow_text}</p>
    </div>
    """)

st.divider()

st.header("Today's Plan")
plan = today_plan(data)
if plan:
    for i, item in enumerate(plan, 1):
        st.markdown(f"**{i}. {item}**")
    else:
        st.markdown("There are no tasks scheduled for today. Enjoy your leisure time or add some activities to your schedule!")

st.divider()
                                        
                                         