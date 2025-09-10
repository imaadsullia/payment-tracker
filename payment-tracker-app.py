import os
import subprocess
import sys

# This section ensures that all necessary packages are installed at runtime.
# This is a workaround for a deployment issue.
def install_dependencies():
    required_packages = ["gspread", "google-auth", "oauth2client"]
    for package in required_packages:
        try:
            __import__(package)
            print(f"'{package}' is already installed.")
        except ImportError:
            print(f"'{package}' not found. Installing now...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"Successfully installed '{package}'.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to install '{package}': {e}")
                sys.exit(1) # Exit if an essential package fails to install

install_dependencies()

# ---------------------------------------------------------------------------------------
# START OF YOUR ORIGINAL APP CODE
# Please paste your original app's code below this line,
# starting with 'import gspread' and all your other logic.
# ---------------------------------------------------------------------------------------

import gspread
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# Use a Streamlit secrets file for credentials
try:
    credentials_dict = st.secrets["gcp_service_account"]
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open_by_key("1XyGg-tP6F1K9eB7P1Y0B8D9E0G2F5A3B4C5D6E7F8")
    worksheet = sheet.worksheet("Payments")
    
    st.title('Payment Tracker')
    st.header('Track your payments in Google Sheets')
    
    # Form for adding new payments
    with st.form(key='payment_form', clear_on_submit=True):
        payer_name = st.text_input('Payer Name')
        amount = st.number_input('Amount', min_value=0.01)
        payment_date = st.date_input('Date', value=date.today())
        
        # Add a submit button
        submit_button = st.form_submit_button(label='Add Payment')
        
    if submit_button:
        if payer_name and amount:
            # Append data to the Google Sheet
            worksheet.append_row([payer_name, amount, str(payment_date)])
            st.success('Payment added successfully!')
        else:
            st.error('Please fill in all the fields.')

    # Display existing payments
    st.subheader('Existing Payments')
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    st.dataframe(df)

except Exception as e:
    st.error(f"An error occurred: {e}")
    st.info("Please ensure your 'secrets.toml' file is correctly configured.")

# ---------------------------------------------------------------------------------------
# END OF YOUR ORIGINAL APP CODE
# You can add more of your original code here if needed.
# ---------------------------------------------------------------------------------------
