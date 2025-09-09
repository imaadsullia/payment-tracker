import streamlit

import pandas as pd
import numpy as np
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Define the scope (permissions)
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# Load service account credentials
creds = Credentials.from_service_account_file("payments.json", scopes=scope)

# Authorize client
client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("payments").sheet1

# Example: Get all data
data = sheet.get_all_records()
df = pd.DataFrame(data)
print(df.head())

# Streamlit app
st.title("🚍 Payment Tracker")
st.write("All customer payment records:")

# Display DataFrame in Streamlit
st.dataframe(df)





