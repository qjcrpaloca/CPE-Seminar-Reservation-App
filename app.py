import streamlit as st
import pandas as pd
import os
from datetime import datetime

page_bg_img = '''
<style>
.main {
background-image: url("https://scontent.fcrk3-2.fna.fbcdn.net/v/t39.30808-6/455816550_926358986197698_7998009224246965628_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=6ee11a&_nc_eui2=AeGmgGAJ-YIQLeX-ZFQq249yv69jAhffUAS_r2MCF99QBKU1mwYrBmx9qSpQ6QUiJkkM-Jl4G7mE8ambWcMK3-qY&_nc_ohc=NzrdNLdsV-cQ7kNvgGLY0f2&_nc_zt=23&_nc_ht=scontent.fcrk3-2.fna&oh=00_AYDl3A89DluBNHNCr3Wo9JyasNb4xL_ahd_GYOcyo5EL4g&oe=66E767DE");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: local;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.logo('cpelogo.jpg',icon_image='cpelogo.jpg')
st.sidebar.image('cpe2.png', use_column_width=True)
st.sidebar.title(':blue[CPE Seminar Reservation]')
st.sidebar.divider()

# Define the file paths
SEMINAR_DATA_FILE = 'seminars.csv'
RESERVATION_DATA_FILE = 'reservations.csv'

# Load seminar data from CSV file
def load_seminar_data():
    if os.path.exists(SEMINAR_DATA_FILE):
        return pd.read_csv(SEMINAR_DATA_FILE)
    else:
        return pd.DataFrame(columns=[':blue[Seminar]', ':blue[Available Spots]', ':blue[Reserved Spots]', ':blue[Date]', ':blue[Start Time]', ':blue[End Time]', ':blue[Location]'])

# Load reservation data from CSV file
def load_reservation_data():
    if os.path.exists(RESERVATION_DATA_FILE):
        return pd.read_csv(RESERVATION_DATA_FILE)
    else:
        return pd.DataFrame(columns=['Seminar', 'Email', 'Student ID'])

# Save seminar data to CSV file
def save_seminar_data(data):
    data.to_csv(SEMINAR_DATA_FILE, index=False)

# Save reservation data to CSV file
def save_reservation_data(data):
    data.to_csv(RESERVATION_DATA_FILE, index=False)

# Initialize session state for seminar data and authentication
if 'seminars' not in st.session_state:
    st.session_state.seminars = load_seminar_data()

if 'reservations' not in st.session_state:
    st.session_state.reservations = load_reservation_data()

if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if 'menu' not in st.session_state:
    st.session_state.menu = "Guest"  # Default to Guest view

def format_time_12h(time):
    """Convert 24-hour time to 12-hour AM/PM format."""
    return time.strftime("%I:%M %p")

def add_seminar(name, spots, date, start_time, end_time, location):
    if name and spots > 0:
        # Convert times to 24-hour format for storage
        start_time_24 = start_time.strftime('%H:%M:%S')
        end_time_24 = end_time.strftime('%H:%M:%S')
        
        new_seminar = pd.DataFrame([[name, spots, 0, date, start_time_24, end_time_24, location]], 
                                   columns=['Seminar', 'Available Spots', 'Reserved Spots', 'Date', 'Start Time', 'End Time', 'Location'])
        st.session_state.seminars = pd.concat([st.session_state.seminars, new_seminar], ignore_index=True)
        save_seminar_data(st.session_state.seminars)
        st.success(f'Seminar "{name}" added successfully!')

def remove_seminar(name):
    st.session_state.seminars = st.session_state.seminars[st.session_state.seminars['Seminar'] != name]
    st.session_state.reservations = st.session_state.reservations[st.session_state.reservations['Seminar'] != name]
    save_seminar_data(st.session_state.seminars)
    save_reservation_data(st.session_state.reservations)
    st.success(f'Seminar "{name}" removed successfully!')

def reserve_spot(name, email, student_id):
    # Check if the user has already reserved a spot for this seminar
    already_reserved = st.session_state.reservations[
        (st.session_state.reservations['Seminar'] == name) & 
        ((st.session_state.reservations['Email'] == email) | 
         (st.session_state.reservations['Student ID'] == student_id))
    ]
    
    if not already_reserved.empty:
        st.warning(f"You have already reserved a spot for seminar '{name}'.")
        return  # Do not proceed further
    
    # Proceed with reservation if not already reserved
    idx = st.session_state.seminars[st.session_state.seminars['Seminar'] == name].index
    if not idx.empty:
        idx = idx[0]
        if st.session_state.seminars.at[idx, 'Available Spots'] > st.session_state.seminars.at[idx, 'Reserved Spots']:
            # Update reservation information
            new_reservation = pd.DataFrame([[name, email, student_id]], columns=['Seminar', 'Email', 'Student ID'])
            st.session_state.reservations = pd.concat([st.session_state.reservations, new_reservation], ignore_index=True)
            st.session_state.seminars.at[idx, 'Reserved Spots'] += 1
            save_seminar_data(st.session_state.seminars)
            save_reservation_data(st.session_state.reservations)
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
        st.session_state.menu = "Admin"  # Redirect to Admin Panel
        st.success('Authenticated successfully!')
    else:
        st.warning('Incorrect username or password.')

st.title(':blue[CPE Seminar Reservation]')
st.divider()

# Menu selection
if st.session_state.admin_authenticated:
    menu = "Admin"
else:
    menu = st.sidebar.selectbox(":blue[Menu]", ["Guest", "Admin"])

if menu == "Admin":
    if not st.session_state.admin_authenticated:
        st.header(":blue[Admin Login]")
        username = st.text_input(":blue[Username]")
        password = st.text_input(":blue[Password]", type='password')
        
        if st.button(":green[Login]"):
            authenticate_admin(username, password)
        st.stop()
    
    st.header(":blue[Admin Panel]")
    
    # Adding a seminar
    seminar_name = st.text_input(":blue[Seminar Name]")
    seminar_spots = st.number_input(":blue[Available Spots]", min_value=1)
    seminar_date = st.date_input(":blue[Date]")
    seminar_start_time = st.time_input(":blue[Start Time]")
    seminar_end_time = st.time_input(":blue[End Time]")
    seminar_location = st.text_input(":blue[Location]")  # Ensure location input is present
    
    if st.button(":green[Add Seminar]"):
        add_seminar(seminar_name, seminar_spots, seminar_date, seminar_start_time, seminar_end_time, seminar_location)
    
    # Removing a seminar
    st.subheader(":blue[Remove a Seminar]")
    seminar_to_remove = st.selectbox(":blue[Select Seminar to Remove]", st.session_state.seminars['Seminar'].tolist())
    
    if st.button(":green[Remove Seminar]"):
        remove_seminar(seminar_to_remove)
    
    # Viewing reservations for a seminar
    st.subheader(":blue[View Reservations]")
    seminar_to_view = st.selectbox(":blue[Select Seminar to View Reservations]", st.session_state.seminars['Seminar'].tolist())
    
    # Filter reservations for the selected seminar
    reservations_for_seminar = st.session_state.reservations[st.session_state.reservations['Seminar'] == seminar_to_view]
    
    if not reservations_for_seminar.empty:
        st.write(f"Total Reserved Spots: {len(reservations_for_seminar)}")
        st.dataframe(reservations_for_seminar)
    else:
        st.write(f":blue[No reservations found for seminar '{seminar_to_view}'.]")

elif menu == "Guest":
    st.header(":blue[Reserve a Spot]")
    seminars_list = st.session_state.seminars['Seminar'].tolist()
    seminar_to_reserve = st.selectbox(":blue[Choose a Seminar]", seminars_list)
    
    email = st.text_input(":blue[Email]")
    student_id = st.text_input(":blue[Student ID]")
    
    if st.button(":green[Reserve Spot]"):
        if email and student_id:
            reserve_spot(seminar_to_reserve, email, student_id)
        else:
            st.warning('Please enter both email and student ID.')

    st.divider()
    st.subheader(":blue[Current Seminars]")
    seminars_df = st.session_state.seminars.copy()
    seminars_df['Start Time'] = pd.to_datetime(seminars_df['Start Time'], format='%H:%M:%S').apply(format_time_12h)
    seminars_df['End Time'] = pd.to_datetime(seminars_df['End Time'], format='%H:%M:%S').apply(format_time_12h)
    seminars_df = seminars_df.drop(columns=['Time','Reservations'])
    st.dataframe(seminars_df)
