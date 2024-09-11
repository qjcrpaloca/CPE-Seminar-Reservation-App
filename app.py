import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit_authenticator as stauth
import bcrypt

# --- SET UP GOOGLE SHEET ACCESS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("YourGoogleSheetName").sheet1

# Fetch all users data
users_data = sheet.get_all_records()

# Convert the Google Sheet data to the format needed by streamlit_authenticator
credentials = {'usernames': {}}

for user in users_data:
    credentials['usernames'][user['username']] = {
        'password': user['password'],  # Store hashed passwords in the Google Sheet
        'name': user['name']
    }

# --- STREAMLIT AUTHENTICATION ---
authenticator = stauth.Authenticate(
    credentials,
    'some_cookie_name',    # Replace with your cookie name
    'some_cookie_key',     # Replace with your cookie key
    30  # Cookie expiry days
)

# --- LOGIN ---
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.success(f"Welcome, {name}")
    
    if username == "admin":  # Admin-specific access
        st.title("Admin Dashboard")
        st.write("This section is only accessible to admin.")
    else:
        st.title(f"User Dashboard")
        st.write(f"Hello {name}, you are logged in as a user.")
        
elif authentication_status is False:
    st.sidebar.error("Username/password is incorrect")
elif authentication_status is None:
    st.sidebar.info("Please enter your username and password")

# --- SIGNUP ---
if st.sidebar.checkbox('Sign up'):
    st.subheader("Create a new account")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    new_name = st.text_input("Name")
    role = st.selectbox("Role", options=["User", "Admin"])

    if st.button("Sign up"):
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        # Add new user to the Google Sheet
        sheet.append_row([new_username, hashed_password, new_name, role])
        st.write(f"New account created for {new_name} as {role}")

# --- LOGOUT ---
if st.sidebar.button('Logout'):
    authenticator.logout("Logout", "sidebar")
