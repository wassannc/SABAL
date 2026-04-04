FORMS = {
    "Farmer Register": {
        "form_id": "FarmerRegister_NF",
        "columns": ["plot_reg.date","plot_reg.landscape","plot_reg.gp","plot_reg.village","plot_reg.farmer_name","plot_reg.spouse","plot_reg.season","plot_reg.crop_model","plot_reg.main_crop","plot_reg.sowing_date"],
        "landscape_col": "plot_reg.landscape"
    },
    "Activities": {
        "form_id": "Activities-NF",
        "columns": ["Primary_details.date","Primary_details.landscape","Primary_details.gp","Primary_details.village","Primary_details.farmer_name","Primary_details.plot_ext","crop_activity","Nf_activites.nf_inputs","Nf_activites.Other_nf_input","Nf_activites.Qty_other_nfinput"],
        "landscape_col": "Primary_details.landscape"
    },
    "BRC": {
        "form_id": "BRC_Units",
        "columns": ["center"],
        "landscape_col": "table_list_pd.landscape"
    },
    "Micro Enterprizes": {
        "form_id": "Micro Enterprizes",
        "columns": ["center"],
        "landscape_col": "table_list_pd.landscape"
    },
    "Meetings&Trainings": {
        "form_id": "Capacity_building",
        "columns": ["center"],
        "landscape_col": "CB_info.landscape"
    },
    "Intensification of Orchards": {
        "form_id": "Orchards_Intensification",
        "columns": ["center"],
        "landscape_col": "basic_info.landscape"
    },
    "Agri Service Centers": {
        "form_id": "Agri Service Centers",
        "columns": ["center"],
        "landscape_col": "pd.landscape"
    },
    "Large & Small Ruminants": {
        "form_id": "Large_Small_Ruminants",
        "columns": ["center"],
        "landscape_col": "table_list_df.landscape"
    } 
}
