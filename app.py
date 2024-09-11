import streamlit as st
import pandas as pd
import os

# Define the file path for storing seminar data
SEMINAR_DATA_FILE = 'seminars.csv'

# Load seminar data from CSV file
def load_seminar_data():
    if os.path.exists(SEMINAR_DATA_FILE):
        return pd.read_csv(SEMINAR_DATA_FILE)
    else:
        return pd.DataFrame(columns=['Seminar', 'Available Spots', 'Reserved Spots', 'Date', 'Time', 'Location'])

# Save seminar data to CSV file
def save_seminar_data(data):
    data.to_csv(SEMINAR_DATA_FILE, index=False)

# Initialize session state for seminar data and authentication
if 'seminars' not in st.session_state:
    st.session_state.seminars = load_seminar_data()

if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

def add_seminar(name, spots, date, time, location):
    if name and spots > 0:
        new_seminar = pd.DataFrame([[name, spots, 0, date, time, location]], columns=['Seminar', 'Available Spots', 'Reserved Spots', 'Date', 'Time', 'Location'])
        st.session_state.seminars = pd.concat([st.session_state.seminars, new_seminar], ignore_index=True)
        save_seminar_data(st.session_state.seminars)
        st.success(f'Seminar "{name}" added successfully!')

def remove_seminar(name):
    st.session_state.seminars = st.session_state.seminars[st.session_state.seminars['Seminar'] != name]
    save_seminar_data(st.session_state.seminars)
    st.success(f'Seminar "{name}" removed successfully!')

def reserve_spot(name, email, student_id):
    idx = st.session_state.seminars[st.session_state.seminars['Seminar'] == name].index
    if not idx.empty:
        idx = idx[0]
        if st.session_state.seminars.at[idx, 'Available Spots'] > st.session_state.seminars.at[idx, 'Reserved Spots']:
            st.session_state.seminars.at[idx, 'Reserved Spots'] += 1
            save_seminar_data(st.session_state.seminars)
            st.success(f'Reserved a spot for seminar "{name}" for {email} (ID: {student_id})!')
        else:
            st.warning(f'No available spots for seminar "{name}".')
    else:
        st.warning(f'Seminar "{name}" not found.')

def authenticate_admin(username, password):
    # Example credentials
    correct_username = 'admin'
    correct_password = 'password'
    if username == correct_username and password == correct_password:
        st.session_state.admin_authenticated = True
        st.success('Authenticated successfully!')
    else:
        st.warning('Incorrect username or password.')

st.title('Seminar Reservation App')

menu = st.sidebar.radio("Menu", ["Admin", "Guest"])

if menu == "Admin":
    if not st.session_state.admin_authenticated:
        st.header("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        
        if st.button("Login"):
            authenticate_admin(username, password)
        st.stop()
    
    st.header("Admin Panel")
    
    # Adding a seminar
    seminar_name = st.text_input("Seminar Name")
    seminar_spots = st.number_input("Available Spots", min_value=1)
    seminar_date = st.date_input("Date")
    seminar_time = st.time_input("Time")
    seminar_location = st.text_input("Location")
    
    if st.button("Add Seminar"):
        add_seminar(seminar_name, seminar_spots, seminar_date, seminar_time, seminar_location)
    
    # Removing a seminar
    st.subheader("Remove a Seminar")
    seminar_to_remove = st.selectbox("Select Seminar to Remove", st.session_state.seminars['Seminar'].tolist())
    
    if st.button("Remove Seminar"):
        remove_seminar(seminar_to_remove)
    
    st.subheader("Current Seminars")
    st.dataframe(st.session_state.seminars)

elif menu == "Guest":
    st.header("Reserve a Spot")
    seminars_list = st.session_state.seminars['Seminar'].tolist()
    seminar_to_reserve = st.selectbox("Choose a Seminar", seminars_list)
    
    email = st.text_input("Email")
    student_id = st.text_input("Student ID")
    
    if st.button("Reserve Spot"):
        if email and student_id:
            reserve_spot(seminar_to_reserve, email, student_id)
        else:
            st.warning('Please enter both email and student ID.')
    
    st.subheader("Current Seminars")
    st.dataframe(st.session_state.seminars)
