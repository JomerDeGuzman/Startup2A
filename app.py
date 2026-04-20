import streamlit as st

from streamlit_logic import pending_tasks, spend_total, today_plan
from streamlit_story import load_data
from streamlit_ui import render_sidebar

st.set_page_config(page_title='Student Quest', layout='wide')


data = load_data()
render_sidebar(data,active_page='Home')
pending = pending_total(data)
spending = spend_total(data)
left = float(data['daily_budget']) - spending
done_count = len(data['daily_tasks']) - len(pending)
budget_percent = int((spending / float(data['daily_budget'])) * 100) if data['daily_budget'] > 0 else 0

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

            .home-info-card .title {
                margin: 0.35rem 0;



    </style>

            
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            col1.metric("Pending Tasks", len(pending), delta= "to do")
        with col2:
            col2.metric("Completed Tasks", done_count, delta= "done")
        with col3:
            col3.metric("Spend Today", f"${spending:.2f}", delta="none")
        with col4:
            col4.metric("Budget Left", f"${left:.2f}", delta=f"{budget_percent}% used")

        
        st.divider()

        info_col1, info_col2, info_col3 = st.columns([2, 1, 1])

        with info_col1:
            st.markdown(
            <div class="home-info-card" style="background-color: var(--home-card-bg); color: var(--home-card-text); padding: 20px; border-radius 10px; border-left: 4px solid var(--home-card-border); color: var(--home-card-text);">
            <h3 style color: var(--home-profile-title); margin-top: 0;">Profile</h3>
            p style=color: var(--home-note-text); margin-bottom: 0;">Name: {data['student_name']}</p>
            p style="margin-bottom: 0;">Daily Budget: ${data['daily_budget']}</p>
            </div>
            )

        with info_col2:
            st.markdown(
        

        with info_col3:
            st.markdown(
            
            
        with in
            
            
            
            
            """)