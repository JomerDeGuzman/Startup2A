import streamlit as st

st.sidebar.title('Navigation')
selected_page = st.sidebar.selectbox(
    'Go to',
    ['Home', 'Profile', 'Tasks', 'Quest Master', 'Settings']
)


# Add filters to sidebar
st.sidebar.header('Filters')
department = st.sidebar.selectbox(
    'Select Department',
    ['Sales', 'Marketing', 'Engineering']
)
date_range = st.sidebar.date_input('Select Date Range')

# Main content area
st.title(f'Page: {selected_page}')
st.write(f'Department: {department}')

