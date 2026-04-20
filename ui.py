import streamlit as st

def render_sidebar(data=None, active_page=None, show_sidebar=True):
    st.markdown(
        """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,)
    
    # If show_sidebar is False, don't render any sidebar content
    if not show_sidebar or data is None:
        return

    current_page = active_page or st.session_state.get("current_page", "Home")
    budget = float(data.get("daily_budget", 0.0) or 0.0)
    coins = int(data.get("coins", 0) or 0)
    level = int(data.get("level", 1) or 1)
    mood = data.get("mood", "Okay")
    student_name = data.get("student_name", "Student")
    tomorrow_needs = data.get("tomorrow_needs", "")
    pending_tasks = [task for task in data.get("tasks", []) if not task.get("done")]
    spent = sum(float(expense.get("amount", 0) or 0) for expense in data.get("expenses", []))
    left = max(0, budget - spent)

    st.sidebar.markdown("""
                        <div style="padding: 0.9rem; border-radius: 0.9rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; margin-bottom: 0.9rem;">
                            <div style="font-size: 0.8rem; opacity: 0.9;">Notes</div>
                            <div style="font-size: 1.15rem; font-weight: 700;">Quest</div>
                        </div>
                        """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
                        <div style="padding: 0.85rem 1rem; border-radius: 0.8rem; border: 1px solid rbga(127, 127, 127, 0.25); margin-bottom: 0.85rem; background rgba(127, 127, 127, 0.06);">
                            <div stle="font-weight: 700; margin-bottom: 0.25rem; color: var(--text-color);">Hello, <span style="color: #f59e0b;">{student_name or 'Student'}</span>!</div>
                            <div (style="font-size: 0.9rem; color: var(--text-color);">Mood: <span style="font-weight: bold; color: #ef4444;">{mood}</span></div>
                            <div style="font-size: 0.9rem; color: var(--text-color);">Level: <span style="font-weight: bold; color: #f59e0b;">{level}  Coins: {coins}</span></div>
                        </div>
                        """,unsafe_allow_html=True)
    

    st.sidebar.metric("Pending Quests", len(pending_tasks))
    st.sidebar.metric("Today's Budget", f"₱{budget:.2f}")

    if budget > 0:
        st.sidebar.progress(min(1.0, spent / budget), text=f"Budget Used: {int((spent / budget) * 100)}%")

    st.sidebar.markdown("""Navigation""")
    st.sidebar.page_link("pages/0_Dashboard.py", label="Home")
    st.sidebar.page_link("pages/1_Profile.py", label="Profile")
    st.sidebar.page_link("pages/2_Tasks.py", label="Tasks")
    st.sidebar.page_link("pages/3_Expenses.py", label="Expenses")
    st.sidebar.page_link("pages/4_Quest_Master.py", label="Quests")
    st.sidebar.page_link("pages/5_Settings.py", label="Settings")
    

    if tomorrow_needs:
        st.sidebar.write(f"Tomorrow's Needs: {tomorrow_needs}")
    else:
        st.sidebar.write("No specific needs for tomorrow yet.")




