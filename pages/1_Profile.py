import streamlit as st

from store import load_data, save_data
from ui import render_sidebar

st.set_page_config(page_title='Profile - Student Quest', layout='wide')

st.title("Profile")

data = load_data()
render_sidebar(data, active_page='Profile')

with st.form("profile_form", border=True):
    st.markdown("### Basic Information")
    student_name = st.text_input("Student Name", value=data.get("student_name", ""), help="Enter your name or nickname.")

    st.markdown("### Budget")
    daily_budget = st.number_input("Daily Budget", min_value=0.0, value=float(data.get("daily_budget", 0)), step=10.0, help="Set your daily budget for tracking expenses.")

    st.markdown("### Current Mood")
    moods = ["Focused", "Okay", "Tired", "Stressed"]        
    mood_value = data["mood"]
    mood_emoji_map = {"Focused": "", "Okay": "", "Tired": "", "Stressed": ""}
    mood_display = mood_emoji_map.get(mood_value, "")
    mood_idx = moods.index(mood_display) if mood_display in moods else 1
    mood_selected = st.selectbox("Current Mood", moods, index=mood_idx)
    mood = mood_selected.split()[-1]

    st.markdown("### Tomorrow's Preparations")
    tomorrow_needs = st.text_area("Tomorrow's Needs", value=data["tomorrow_needs"], height=120, help="write down any preparations, tasks, or goals you have for tomorrow.")

    submitted = st.form_submit_button("Save Profile", use_container_width=True)

    if submitted:
        data["student_name"] = student_name.strip() or  "Student"
        data["daily_budget"] = float(daily_budget)
        data["mood"] = mood
        data["tomorrow_needs"] = tomorrow_needs.strip()
        save_data(data)
        st.success("Profile saved successfully!")
        st.balloons()


    with st.expander("About your Profile"):
        st.markdown(
            """
            - **Student Name**: This is your name or nickname that will be displayed in the sidebar and used to personalize your experience.
            - **Daily Budget**: Set a daily budget to track your expenses. This helps you manage your finances and stay on top of your spending habits.
            - **Current Mood**: Select how you're feeling today. This can help you reflect on your emotional state and how it may impact your productivity.
            - **Tomorrow's Needs**: Use this space to jot down any preparations, tasks, or goals you have for tomorrow. This can help you plan ahead and stay organized.
            """
        )