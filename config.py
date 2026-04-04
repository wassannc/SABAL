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
        "columns": ["SubmissionDate","table_list_pd.landscape","table_list_pd.brc_unit","table_list_pd.product_name","table_list_pd.brc_sale_date","table_list_pd.dj_sale_farmer","table_list_pd.gender","table_list_pd.sale_village","table_list_sd.sale_qty","table_list_sd.total_income","table_list_cd.crops","table_list_cd.crop_ext"],
        "landscape_col": "table_list_pd.landscape"
    },
    "Micro Enterprizes": {
        "form_id": "Micro Enterprizes",
        "columns": ["SubmissionDate","table_list_pd.landscape","table_list_pd.gp","table_list_pd.village","table_list_pd1.farmer_name","table_list_pd1.processing_hub_tool","table_list_pd1.processing_date","table_list_pd1.processed_for","table_list_pd2.processing_farmer_village","table_list_pd2.processing_farmer","table_list_pd2.processing_qty_kgs","table_list_pd2.rent_amount","table_list_pd3.Data_sub_by"],
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
