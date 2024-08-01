import streamlit as st 
from indicators import download_all_indicators
from country_facts import fetch_and_cache_countries_data
import os
import shutil

# st.button("Download all indicators", on_click=download_all_indicators("lldcs"))

st.button("Fetch and cache countries data", on_click=fetch_and_cache_countries_data)

def copy_json_files():
    parent_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "factbook.json")
    destination_folder = "factbook"
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".json"):
                source_path = os.path.join(root, file)
                shutil.copy(source_path, destination_folder)
    
    print("JSON files copied successfully!")


