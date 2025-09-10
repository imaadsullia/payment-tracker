import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from Streamlit Secrets
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"]
)

client = gspread.authorize(creds)

# Open your Google Sheet
sheet = client.open("payments").sheet1

# Convert sheet data to DataFrame
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("🚍 Payment Tracker")

st.write("Here are the current payments:")
st.dataframe(df)
