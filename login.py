# ===== DEBUGGED BY AI =====
# Fixed authentication flow with session state
# Now uses MySQL database (sas_db) to verify user credentials
# Redirects to pages/home.py after successful login
# Added user registration functionality

import streamlit as st
from database import DatabaseConnection
from db_config import DB_CONFIG

st.set_page_config(page_title='Survive-A-Semester', layout='centered')

# Hide sidebar completely
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "show_register" not in st.session_state:
    st.session_state.show_register = False

def check_login(username, password):
    """Check login credentials against MySQL database"""
    try:
        db = DatabaseConnection(**DB_CONFIG)
        if db.connect():
            result = db.verify_user(username, password)
            db.disconnect()
            return result
        else:
            st.error("❌ Database connection failed!")
            st.info("📝 Setup Instructions:\n1. Run: `python diagnose_db.py`\n2. Run: `python setup_database.py`\n3. Try login again")
            return False
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        st.info("💡 Run `python diagnose_db.py` to troubleshoot")
        return False

def register_user(username, password, email):
    """Register a new user in the database"""
    try:
        db = DatabaseConnection(**DB_CONFIG)
        if db.connect():
            # Check if user already exists
            if db.user_exists(username):
                st.error(f"❌ Username '{username}' already exists!")
                db.disconnect()
                return False
            
            # Register the user
            result = db.register_user(username, password, email)
            db.disconnect()
            
            if result:
                st.success(f"✅ Account created successfully for '{username}'!")
                st.info("You can now login with your credentials.")
                return True
            else:
                st.error("❌ Failed to create account. Please try again.")
                return False
        else:
            st.error("❌ Database connection failed!")
            return False
    except Exception as e:
        st.error(f"❌ Registration Error: {e}")
        return False

def login_page():
    st.title("Survive-A-Semester")
    st.markdown("Complete quests to survive!")
    st.markdown("---")
    
    # Login section
    st.subheader("Login")
    username = st.text_input("Username", key="credentials")
    password = st.text_input("Password", type='password', key="credential")
    
    if st.button("Login", use_container_width=True):
        if username and password:
            if check_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully!")
                st.switch_page("pages/0_Dashboard.py")
            else:
                st.error("❌ Invalid credentials")
        else:
            st.warning("⚠️ Please enter both username and password")
    
    st.markdown("---")
    
    # Toggle to registration
    if st.button("Don't have an account? Register here", use_container_width=True):
        st.session_state.show_register = True
        st.rerun()
    
    st.markdown("---")
    

def register_page():
    st.title("Survive-A-Semester")
    st.markdown("Create your account to survive!")
    st.markdown("---")
    
    # Registration section
    st.subheader("Create Account")
    
    reg_username = st.text_input("Choose a username", key="reg_username")
    reg_email = st.text_input("Email address", key="reg_email")
    reg_password = st.text_input("Create a password", type='password', key="reg_password")
    reg_password_confirm = st.text_input("Confirm password", type='password', key="reg_password_confirm")
    
    if st.button("Register", use_container_width=True):
        # Validation
        if not all([reg_username, reg_email, reg_password, reg_password_confirm]):
            st.warning("⚠️ Please fill in all fields")
        elif len(reg_username) < 3:
            st.warning("⚠️ Username must be at least 3 characters")
        elif len(reg_password) < 6:
            st.warning("⚠️ Password must be at least 6 characters")
        elif reg_password != reg_password_confirm:
            st.error("❌ Passwords don't match!")
        elif "@" not in reg_email:
            st.warning("⚠️ Please enter a valid email address")
        else:
            # Register the user
            if register_user(reg_username, reg_password, reg_email):
                st.session_state.show_register = False
                st.rerun()
    
    st.markdown("---")
    
    # Toggle back to login
    if st.button("Already have an account? Login here", use_container_width=True):
        st.session_state.show_register = False
        st.rerun()
    
    st.markdown("---")
    st.caption("**Passwords are securely hashed with SHA-256**")

if __name__ == "__main__":
    if st.session_state.logged_in:
        st.switch_page("pages/0_Dashboard.py")
    elif st.session_state.show_register:
        register_page()
    else:
        login_page()