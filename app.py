import streamlit as st
import pandas as pd
import hashlib

# Helper functions
def load_users():
    return pd.read_csv('users - Sheet1.csv')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(stored_password, provided_password):
    return stored_password == hash_password(provided_password)

def signup(username, password, role):
    df = load_users()
    if username in df['username'].values:
        st.error("Username already exists.")
    else:
        new_user = pd.DataFrame([[username, hash_password(password), role]], columns=['username', 'password', 'role'])
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_csv('users.csv', index=False)
        st.success("Signup successful! You can now log in.")

def login(username, password):
    df = load_users()
    user = df[df['username'] == username]
    if user.empty:
        st.error("Username not found.")
    elif check_password(user.iloc[0]['password'], password):
        st.success(f"Login successful! Welcome {user.iloc[0]['role']}.")
    else:
        st.error("Incorrect password.")

# Streamlit app
st.title("Login and Signup System")

menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login Section")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        login(username, password)

elif choice == "Signup":
    st.subheader("Signup Section")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    role = st.selectbox("Role", ["admin", "user"])
    if st.button("Signup"):
        signup(username, password, role)
