import requests
import pandas as pd

ODK_URL = "https://your-odk-url"
PROJECT_ID = "1"

USERNAME = "your_email"
PASSWORD = "your_password"

def load_odk_data(form_id):
    url = f"{ODK_URL}/v1/projects/{PROJECT_ID}/forms/{form_id}.svc/Submissions"
    
    response = requests.get(url, auth=(USERNAME, PASSWORD))
    
    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    
    if "value" not in data:
        return pd.DataFrame()

    df = pd.json_normalize(data["value"])
    
    return df
