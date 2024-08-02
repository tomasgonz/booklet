import streamlit as st 
from indicators import download_all_indicators
from country_facts import fetch_and_cache_countries_data
import os
import shutil

#st.button("Download all indicators for LLDCs", on_click=download_all_indicators("lldcs"))
#st.button("Download all indicators for LDCs", on_click=download_all_indicators("ldcs"))
#st.button("Download all indicators for SIDS", on_click=download_all_indicators("sids"))
#st.button("Fetch and cache countries data", on_click=fetch_and_cache_countries_data)

def copy_json_files():
    parent_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "factbook.json")
    destination_folder = "./cache/factbook"
    
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            if file.endswith(".json"):
                source_path = os.path.join(root, file)
                shutil.copy(source_path, destination_folder)
    
    print("JSON files copied successfully!")

def copy_map_files():
    parent_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "./mapsicon/all")
    destination_folder = "./cache/maps"
    
    folders = [folder for folder in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, folder))]

    for folder in folders:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        
        for root, dirs, files in os.walk(os.path.join(parent_folder, folder)):
            for file in files:
                if file.endswith(".png") or file.endswith(".svg"):
                    source_path = os.path.join(root, file)
                    destination_file = folder + "_" + file
                    final_destination = os.path.join(destination_folder, destination_file)
                    shutil.copy(source_path, final_destination)

    st.write(folders)

    st.write("Map files copied successfully!")


