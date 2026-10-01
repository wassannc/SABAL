import streamlit as st
import requests
import pandas as pd

ODK_URL = st.secrets["ODK_URL"]
USERNAME = st.secrets["USERNAME"]
PASSWORD = st.secrets["PASSWORD"]
PROJECT_ID = st.secrets["PROJECT_ID"]

@st.cache_data(ttl=600)
def load_odk_data(form_id):

    url = f"{ODK_URL}/projects/{PROJECT_ID}/forms/{form_id}.svc/Submissions"

    response = requests.get(
        url,
        auth=(USERNAME, PASSWORD)
    )

    if response.status_code != 200:
        st.error(f"Error: {response.status_code}")
        return pd.DataFrame()

    data = response.json()

    if "value" not in data:
        return pd.DataFrame()

    df = pd.json_normalize(data["value"])

    return df
# ---------------- GOOGLE SHEET ----------------

import gspread
from google.oauth2.service_account import Credentials

SHEET_ID = "YOUR_EXISTING_GOOGLE_SHEET_ID"

@st.cache_data(ttl=600)
def load_google_sheet(sheet_name):

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(SHEET_ID)
    worksheet = spreadsheet.worksheet(sheet_name)

    data = worksheet.get_all_records()

    return pd.DataFrame(data)
