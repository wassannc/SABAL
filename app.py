import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
from datetime import date
from config import FORMS
from utils import load_odk_data
def clean_landscape(series):
    return series.replace({
        "KG.Pudi": "KG Pudi",
        "KG Pudu": "KG Pudi",
        "Kg Pudi": "KG Pudi",
        "Kg Pudu": "KG Pudi",
        "Kgpudi": "KG Pudi"
    })
def push_to_google_sheet(df):

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("Reminder_SABAL").worksheet("Data")

    # 🔥 SAFE CONVERSION
    df = df.fillna("").astype(str)

    # Prepare data
    data = [df.columns.values.tolist()] + df.values.tolist()

    # Clear sheet
    sheet.clear()

    # Upload in chunks (prevents error)
    chunk_size = 5000

    for i in range(0, len(data), chunk_size):
        sheet.update(
            f"A{i+1}",
            data[i:i+chunk_size]
        ) 

st.sidebar.title("Menu")

main_section = st.sidebar.radio(
    "Select Section",
    ["MIS-Status", "MIS-Reports", "Landscape profiles", "Dashboards"]
)

if main_section == "MIS-Reports":
    page = st.sidebar.radio(
        "Select Form",
        list(FORMS.keys())
    )
else:
    page = main_section  
    
 # ---------------- FILTERS ----------------
    import calendar
    col1, col2 = st.columns(2)

    with col1:
        all_landscapes = set()

        for form_name, config in FORMS.items():
            df_temp = load_odk_data(config["form_id"])
            col = config.get("landscape_col")
            if col and col in df_temp.columns:
                df_temp[col] = clean_landscape(df_temp[col])
            
            if col and col in df_temp.columns:
                all_landscapes.update(df_temp[col].dropna().unique())

        all_landscapes = sorted(all_landscapes)

        selected_landscape = st.selectbox(
            "Select Landscape",
            ["All"] + list(all_landscapes)
        )

    with col2:
        months = ["All"] + [calendar.month_name[i] for i in range(1, 13)]
        selected_month = st.selectbox("Select Month", months)
        
if page == "MIS-Status":
    import pandas as pd
    import calendar

    st.title(" MIS Status")
    today = str(date.today())

    # Check last sync date
    if "last_sync" not in st.session_state:
        st.session_state["last_sync"] = ""

    if st.session_state["last_sync"] != today:

        with st.spinner("🔄 Auto syncing data..."):

            all_data = []

            for form_name, config in FORMS.items():
                df = load_odk_data(config["form_id"])

                if df.empty:
                    continue

                landscape_col = config.get("landscape_col")

                if landscape_col in df.columns:
                    landscape = clean_landscape(df[landscape_col])
                else:
                    landscape = "Unknown"

                date_series = None
                for col in ["__system.submissionDate", "meta.submissionDate"]:
                    if col in df.columns:
                        date_series = pd.to_datetime(df[col], errors="coerce")
                        break

                if date_series is None:
                    continue

                temp_df = pd.DataFrame({
                    "Landscape": landscape,
                    "Date": date_series,
                    "Form": form_name
                })

                temp_df["Month"] = temp_df["Date"].dt.to_period("M").astype(str)

                temp_df = (
                    temp_df
                    .groupby(["Landscape", "Month", "Form"])
                    .size()
                    .reset_index(name="Count")
                )

                all_data.append(temp_df)

            if all_data:
                final_df = pd.concat(all_data, ignore_index=True)

                current_month = str(pd.Timestamp.now().to_period("M"))
                final_df = final_df[final_df["Month"] == current_month]

                final_df = final_df.sort_values(["Month", "Landscape", "Form"])

                push_to_google_sheet(final_df)

                st.session_state["last_sync"] = today

                st.success("✅ Auto sync completed!")

            else:
                st.warning("No data available to sync")

    # ---------------- DATA DISPLAY ----------------
    forms_list = list(FORMS.items())
    cols_per_row = 2

    for i in range(0, len(forms_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if i + j >= len(forms_list):
                break

            form_name, config = forms_list[i + j]
            df = load_odk_data(config["form_id"])
            landscape_col = config.get("landscape_col")
            if landscape_col in df.columns:
                df[landscape_col] = clean_landscape(df[landscape_col])
            
            # -------- APPLY FILTERS --------

            # Landscape filter
            if selected_landscape != "All" and landscape_col in df.columns:
                df = df[df[landscape_col] == selected_landscape]

            # Month filter
            date_cols = ["__system.submissionDate", "meta.submissionDate"]
            date_col = None

            for col in date_cols:
                if col in df.columns:
                    date_col = col
                    break

            if selected_month != "All" and date_col:
                df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
                month_num = list(calendar.month_name).index(selected_month)
                df = df[df[date_col].dt.month == month_num]

            # -------- UI --------
            with cols[j]:
                st.markdown(f"#### 📦 {form_name}")

                if df.empty:
                    st.write("No data")
                    continue

                st.caption(f"Total: {len(df)}")

                if landscape_col and landscape_col in df.columns:
                    grouped = (
                        df.groupby(landscape_col)
                        .size()
                        .reset_index(name="Count")
                        .sort_values("Count", ascending=False)
                    )

                    grouped.columns = ["Landscape", "Count"]

                    st.dataframe(grouped, use_container_width=True, height=200)

                else:
                    st.warning(f"{landscape_col} not found")
                    
elif page == "Landscape profiles":
    st.title("📊 Landscape Profiles")
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(creds)
    worksheet = client.open("Reminder_SABAL").worksheet("progress")
    all_data = worksheet.get_all_values()
    headers = all_data[0]
    rows = all_data[1:]
    df = pd.DataFrame(rows, columns=headers)
    
    # Apply Landscape Filter
    if selected_landscape != "All":
        df = df[df["Landscape"] == selected_landscape]
        
    # Convert numeric columns
    numeric_cols = [
        "Total HH",
        "No of SHG groups",
        "Total Landless HH",
        "Total Geography in acre",
        "Total Forest land in acres",
        "Total Common land ( Panchayat/ revenue forest land) in acres",
        "Total Orchard lands in acres",
        "Total HH own Orchards",
        "Total HH who has eco intensified their orchards"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            st.warning(f"Column not found: {col}")
            
    st.subheader("📈 Overview")
    demo = (
        df.groupby("Landscape")
        .agg(
            Total_Villages=("Village", "nunique"),
            Total_HHs=("Total HH", "sum"),
            Total_SHGs=("No of SHG groups", "sum"),
            Total_Landless_HH=("Total Landless HH", "sum")
        )
        .reset_index()
    )
    total_landscapes = demo["Landscape"].nunique()
    total_villages = int(demo["Total_Villages"].sum())
    total_hhs = int(demo["Total_HHs"].sum())
    total_shgs = int(demo["Total_SHGs"].sum())
    total_landless = int(demo["Total_Landless_HH"].sum())
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🏞 Landscapes", total_landscapes)
    col2.metric("🏘 Villages", total_villages)
    col3.metric("👨‍👩‍👧‍👦 Households", total_hhs)
    col4.metric("👥 SHG Groups", total_shgs)
    col5.metric("🏠 Landless HH", total_landless)

    st.markdown("---")
    st.subheader("📈 Demographical Analysis")
    # Convert Tribal HH percentage
    df["% of tribal HH"] = (
        df["% of tribal HH"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["% of tribal HH"] = pd.to_numeric(
        df["% of tribal HH"],
        errors="coerce"
    )
    tribal = (
        df.groupby("Landscape")["% of tribal HH"]
            .mean()
            .reset_index()
    )
    import plotly.express as px

    fig = px.bar(
        tribal,
        x="% of tribal HH",
        y="Landscape",
        orientation="h",
        text="% of tribal HH",
        title="Tribal Households (%) by Landscape",
        color="% of tribal HH",
        color_continuous_scale="Viridis"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Tribal Households (%)",
        yaxis_title="",
        coloraxis_showscale=False,
        title_x=0.5
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("---")
    st.subheader("🌳 Forest & Common Lands")

    forest = (
        df.groupby("Landscape")
          .agg(
              Geography=("Total Geography in acre","sum"),
              Forest=("Total Forest land in acres","sum"),
              Common=("Total Common land ( Panchayat/ revenue forest land) in acres","sum"),
              Orchard=("Total Orchard lands in acres","sum"),
              Orchard_HH=("Total HH own Orchards","sum"),
              Intensified=("Total HH who has eco intensified their orchards","sum")
          )
          .reset_index()
    )
    forest["Forest %"] = (
        forest["Forest"] / forest["Geography"] * 100
    )

    forest["Common %"] = (
        forest["Common"] / forest["Geography"] * 100
    )

    forest["Orchard %"] = (
        forest["Orchard"] / forest["Geography"] * 100
    )

    forest["HH Intensified %"] = (
        forest["Intensified"] / forest["Orchard_HH"] * 100
    )

    forest = forest.fillna(0)

    fig = px.bar(
        forest,
        x="Forest %",
        y="Landscape",
        orientation="h",
        text="Forest %",
        title="Forest Land (%) by Landscape",
        color="Forest %",
        color_continuous_scale="Greens"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        height=450,
        xaxis_title="Forest Land (%)",
        yaxis_title="",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
    x="Common %"
    title="Common Land (%) by Landscape"
    color="Common %"
    color_continuous_scale="Blues"

    x="HH Intensified %"
    title="HH Intensified Orchards (%)"
    color="HH Intensified %"
    color_continuous_scale="Purples"
    
elif page == "Dashboards":

    st.title("📊 SABAL Dashboards")

    # Dropdown
    dashboard_option = st.selectbox(
        "Select Dashboard",
        [
            "NF-Trails",
            "Bio Resource Centers",
            "Capacity Building",
            "Coffee Plots",
            "Gender"
        ]
    )

    # Links mapping
    dashboard_links = {
        "NF-Trails": "https://app.powerbi.com/view?r=eyJrIjoiMjk4OTUxMGUtYjBjMS00YWEyLWEwZmUtMTVkNGI0M2EwZWQxIiwidCI6IjQ5NTM2MmE3LTQxMjItNDQ0OC1iNGU2LTIxYzQzZTRiZjRmZCJ9",
        "Bio Resource Centers": "https://app.powerbi.com/view?r=eyJrIjoiN2YzM2ZhM2QtZTUzOC00ZTRkLTllN2EtNDFmNDg5MDhiNTIwIiwidCI6IjQ5NTM2MmE3LTQxMjItNDQ0OC1iNGU2LTIxYzQzZTRiZjRmZCJ9",
        "Capacity Building": "https://app.powerbi.com/view?r=eyJrIjoiMTBjNjY4MWMtMTZhMi00ZDViLWE4OTQtYjNmM2I2MzVkMGVlIiwidCI6IjQ5NTM2MmE3LTQxMjItNDQ0OC1iNGU2LTIxYzQzZTRiZjRmZCJ9",
        "Coffee Plots": "https://app.powerbi.com/view?r=eyJrIjoiOTNjZDI5NzktYWJiMS00ZmUxLWE4ZWEtZDE0MjQzYWY3MzQzIiwidCI6IjQ5NTM2MmE3LTQxMjItNDQ0OC1iNGU2LTIxYzQzZTRiZjRmZCJ9&pageName=e08ee9a2644d492a41a5",
        "Gender": "https://app.powerbi.com/view?r=eyJrIjoiNzZiNWQ0NDYtZmVkNi00NWVlLThhZTctYTEzYjg3NmUyNGE5IiwidCI6IjQ5NTM2MmE3LTQxMjItNDQ0OC1iNGU2LTIxYzQzZTRiZjRmZCJ9"
    }

    st.components.v1.iframe(
    dashboard_links[dashboard_option],
    height=700,
    scrolling=True
) 
    
elif page in FORMS:
    st.title(f"📥 {page}")

    config = FORMS[page]
    df = load_odk_data(config["form_id"])
            
    if df.empty:
        st.warning("No data found")
    
    else:
        # Select only required columns
        columns = config.get("columns", [])
        available_cols = [col for col in columns if col in df.columns]

        df_filtered = df[available_cols]
        column_labels = config.get("column_labels", {})
        df_filtered = df_filtered.rename(columns=column_labels)
        st.dataframe(df_filtered, use_container_width=True)
        
        # Download button
        st.download_button(
            label="⬇ Download CSV",
            data=df_filtered.to_csv(index=False),
            file_name=f"{page}_report.csv",
            mime="text/csv"
        )
