import streamlit as st
def login_page():
    st.title("Survive-A-Semester")
    st.markdown("Complete quests to survive!")
    
    username = st.text_input("Username", key="credentials")
    password = st.text_input("Password", type='password', key="credential")
    if st.button("Login"):
        if check_login(username, password):  # You would define check_login based on your criteria
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials")

def check_login(username, password):
    # Replace this with your actual login logic (database, API calls, etc.)
    return username == "admin" and password == "password"

if __name__ == "__main__":
    login_page()

st.markdown(
"""
<style>

.body {
background-color: black;
}

.st-key-title title{
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
font-size: 40px;
}

</style>
"""
,unsafe_allow_html=True
)
