import requests
import json
import os

# Define the file path for caching
cache_dir = './cache'
cache_file = os.path.join(cache_dir, 'country_facts.json')

def fetch_and_cache_countries_data():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    countries = response.json()
    
    # Ensure the cache directory exists
    os.makedirs(cache_dir, exist_ok=True)
    
    # Save data to cache file
    with open(cache_file, 'w') as file:
        json.dump(countries, file, indent=4)
    
    return countries

def load_countries_data():
    # Check if the cache file exists
    if os.path.exists(cache_file):
        # Load data from cache file
        with open(cache_file, 'r') as file:
            countries = json.load(file)
    else:
        # Fetch and cache the data if cache file doesn't exist
        countries = fetch_and_cache_countries_data()
    
    return countries

def load_countries_group_data(group):
    data = load_countries_data()
    return [country for country in data if country['cca3'] in group]

def load_country_data(country_code):
    data = load_countries_data()
    return [country for country in data if country['cca3'] == country_code]

def load_factbook_data(country_code):
    filename = f"{country_code.lower()}.json"
    file_path = os.path.join("cache/factbook",  filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
    
def load_small_flags():
    data = load_countries_data()
    return [{"cca3":country['cca3'], "flag": country['flag']} for country in data]

def get_small_flag(cca3):
    for item in country_small_flags:
        if item['cca3'] == cca3:
            return item['flag']
        
def load_country_qualitative_info():
    filename = "countries.json"
    file_path = os.path.join("cache",  filename)
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def get_country_description(iso3):
    for item in country_qualitative_data:
        if item['iso3'] == iso3:
            return item['profile']

country_qualitative_data = load_country_qualitative_info()

country_small_flags = load_small_flags()