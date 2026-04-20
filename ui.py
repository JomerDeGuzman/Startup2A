import streamlit as st


def render_sidebar(data, active_page="Home"):
	st.sidebar.title("Student Quest")
	st.sidebar.caption(f"Page: {active_page}")

	name = str(data.get("student_name", "")).strip() or "Student"
	mood = str(data.get("mood", "")).strip() or "Okay"

	st.sidebar.write(f"Name: {name}")
	st.sidebar.write(f"Mood: {mood}")
