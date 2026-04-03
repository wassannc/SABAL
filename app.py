import streamlit as st
from config import FORMS
from utils import load_odk_data

st.set_page_config(page_title="Project Dashboard", layout="wide")

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["MIS-Status", "MIS-Reports"])

# ---------------- DASHBOARD ----------------
if page == "MIS-Status":
    st.title("📊 Project Progress")

    cols = st.columns(3)

    i = 0
    for form_name, config in FORMS.items():
        df = load_odk_data(config["form_id"])
        
        with cols[i % 3]:
            st.metric(form_name, len(df))
        
        i += 1


# ---------------- DOWNLOADS ----------------
elif page == "MIS-Reports":
    st.title("📥 Download Data")

    form_name = st.selectbox("Select Form", list(FORMS.keys()))
    
    config = FORMS[form_name]
    df = load_odk_data(config["form_id"])

    if df.empty:
        st.warning("No data found")
    else:
        columns = config["columns"]
        
        available_cols = [col for col in columns if col in df.columns]
        df_filtered = df[available_cols]

        st.dataframe(df_filtered)

        st.download_button(
            "Download CSV",
            df_filtered.to_csv(index=False),
            f"{form_name}.csv",
            "text/csv"
        )
