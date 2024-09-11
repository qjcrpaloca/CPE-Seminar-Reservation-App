import streamlit as st
import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('database - Sheet 1.csv')

# Display the DataFrame
st.write(df)
