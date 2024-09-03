import os
import json

# Load the country codes
country_codes = []

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_groups_from_json_files(directory):
    groups = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            json_data = load_json_file(file_path)
            groups.append(json_data)
    return groups

def get_group_countries_iso3(group):
    filename = f"{group}.json"
    file_path = os.path.join(cache_folder, filename)
    group_list = load_json_file(file_path)
    countries = [country['ISO3'] for country in group_list['countries']]
    names = [country['name'] for country in group_list['countries']]
    return countries

def get_group_countries_iso2(group):
    filename = f"{group}.json"
    file_path = os.path.join(cache_folder, filename)
    group_list = load_json_file(file_path)
    countries = [country['ISO'] for country in group_list['countries']]
    return countries

def get_group_countries_name(group):
    filename = f"{group}.json"
    file_path = os.path.join(cache_folder, filename)
    group_list = load_json_file(file_path)
    countries = [country['name'] for country in group_list['countries']]
    return countries

def get_iso3_from_name(name, group):
    filename = f"{group}.json"
    file_path = os.path.join(cache_folder, filename)
    group_list = load_json_file(file_path)
    iso3 = [country['ISO3'] for country in group_list['countries'] if country['name'] == name]
    return iso3[0] if iso3 else None

def get_iso2_from_name(name):
    for country in country_codes:
        if country['NAME.EN'] == name:
            return country['ISO_3166_2']
    return None

def get_name_from_iso3(iso3):
    for country in country_codes:
        if country['ISO_3166_3'] == iso3:
            return country['NAME.EN']
    return None

def get_fips_from_iso3(iso3):
    for country in country_codes:
        if country['ISO_3166_3'] == iso3:
            return country['FIPS_GEC']
    return None

def get_iso3_from_fips(fips):
    for country in country_codes:
        if country['FIPS_GEC'] == fips:
            return country['ISO_3166_3']
    return None

def load_country_codes():
    with open('cache/Countrycodesfull.json', 'r', encoding='utf-8') as f:
        country_codes = json.load(f)
    return country_codes

cache_folder = "cache/groups"

country_codes = load_country_codes()