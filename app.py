import streamlit as st
from config import FORMS
from utils import load_odk_data

st.set_page_config(page_title="Project Dashboard", layout="wide")

st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["MIS-Status", "MIS-Reports"])

if page == "MIS-Status":
    import pandas as pd

    st.title("📊 MIS Status")

    forms_list = list(FORMS.items())
    cols_per_row = 2   # 👈 2 boxes per row

    for i in range(0, len(forms_list), cols_per_row):
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            if i + j >= len(forms_list):
                break

            form_name, config = forms_list[i + j]
            df = load_odk_data(config["form_id"])
            landscape_col = config.get("landscape_col")

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

                    # 👇 compact table
                    st.dataframe(
                        grouped,
                        use_container_width=True,
                        height=200   # 👈 limits size
                    )

                else:
                    st.warning(f"{landscape_col} not found")


# ---------------- MIS REPORTS ----------------
elif page == "MIS-Reports":
    st.title("📥 MIS Reports")

    form_name = st.selectbox("Select Form", list(FORMS.keys()))
    config = FORMS[form_name]

    df = load_odk_data(config["form_id"])

    if df.empty:
        st.warning("No data found")
    else:
        available_cols = [col for col in config["columns"] if col in df.columns]
        df_filtered = df[available_cols]

        st.dataframe(df_filtered)

        st.download_button(
            "Download CSV",
            df_filtered.to_csv(index=False),
            f"{form_name}.csv",
            "text/csv"
        )
