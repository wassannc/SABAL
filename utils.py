import streamlit as st
import requests
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

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
# ---------------- E-PRA GOOGLE SHEET ----------------

@st.cache_data(ttl=600)
def load_epra_data():

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)

    worksheet = client.open("Reminder_SABAL").worksheet("ePRA")

    all_data = worksheet.get_all_values()

    if not all_data:
        return pd.DataFrame()

    headers = all_data[0]
    rows = all_data[1:]

    df = pd.DataFrame(rows, columns=headers)

    return df
