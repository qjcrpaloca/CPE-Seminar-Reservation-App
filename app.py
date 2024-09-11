import streamlit as st
import pandas as pd

# Initialize session state for seminar data
if 'seminars' not in st.session_state:
    st.session_state.seminars = pd.DataFrame(columns=['Seminar', 'Available Spots', 'Reserved Spots'])

def add_seminar(name, spots):
    if name and spots > 0:
        new_seminar = pd.DataFrame([[name, spots, 0]], columns=['Seminar', 'Available Spots', 'Reserved Spots'])
        st.session_state.seminars = pd.concat([st.session_state.seminars, new_seminar], ignore_index=True)
        st.success(f'Seminar "{name}" added successfully!')

def reserve_spot(name):
    idx = st.session_state.seminars[st.session_state.seminars['Seminar'] == name].index
    if not idx.empty:
        idx = idx[0]
        if st.session_state.seminars.at[idx, 'Available Spots'] > st.session_state.seminars.at[idx, 'Reserved Spots']:
            st.session_state.seminars.at[idx, 'Reserved Spots'] += 1
            st.success(f'Reserved a spot for seminar "{name}"!')
        else:
            st.warning(f'No available spots for seminar "{name}".')
    else:
        st.warning(f'Seminar "{name}" not found.')

st.title('Seminar Reservation App')

menu = st.sidebar.radio("Menu", ["Admin", "Guest"])

if menu == "Admin":
    st.header("Admin Panel")
    seminar_name = st.text_input("Seminar Name")
    seminar_spots = st.number_input("Available Spots", min_value=1)
    
    if st.button("Add Seminar"):
        add_seminar(seminar_name, seminar_spots)

    st.subheader("Current Seminars")
    st.dataframe(st.session_state.seminars)

elif menu == "Guest":
    st.header("Reserve a Spot")
    seminars_list = st.session_state.seminars['Seminar'].tolist()
    seminar_to_reserve = st.selectbox("Choose a Seminar", seminars_list)

    if st.button("Reserve Spot"):
        reserve_spot(seminar_to_reserve)
    
    st.subheader("Current Seminars")
    st.dataframe(st.session_state.seminars)
