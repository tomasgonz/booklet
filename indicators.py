import requests
import pandas as pd
import datetime
import os
import json
from country_groups.groups import get_group_countries_iso3
from time import sleep

indicators = {
    'SP.POP.TOTL': {
        'source': 'World Bank',
        'description': 'Population, total'
    },
    'NY.GDP.MKTP.PP.CD': {
        'source': 'World Bank',
        'description': 'GDP, PPP (current international $)'
    },
    'NY.GDP.PCAP.PP.CD': {
        'source': 'World Bank',
        'description': 'GDP per capita, PPP (current international $)'
    },
    'AG.SRF.TOTL.K2': {
        'source': 'World Bank',
        'description': 'Surface area (sq. km)'
    },
    'BX.KLT.DINV.WD.GD.ZS': {
        'source': 'World Bank',
        'description': 'Foreign direct investment, net inflows (% of GDP)'
    },
    'BM.KLT.DINV.WD.GD.ZS': {
        'source': 'World Bank',
        'description': 'Foreign direct investment, net outflows (% of GDP)'
    },
    'DT.ODA.ODAT.GN.ZS': {
        'source': 'World Bank',
        'description': 'Net official development assistance received (% of GNI)'
    },
    'LP.LPI.OVRL.XQ': {
        'source': 'World Bank',
        'description': 'Logistics performance index: Overall (1=low to 5=high)'
    },
    'LP.EXP.DURS.MD': {
        'source': 'World Bank',
        'description': 'Time to export, median case (days)'
    },
    'GC.TAX.IMPT.ZS': {
        'source': 'World Bank',
        'description': 'Tax revenue (% of GDP)'
    },
    'IC.IMP.CSBC.CD': {
        'source': 'World Bank',
        'description': 'Imports of goods and services (current US$)'
    },
    'IC.IMP.TMBC': {
        'source': 'World Bank',
        'description': 'Imports of goods and services (BoP, current US$)'
    },
    'IC.EXP.CSBC.CD': {
        'source': 'World Bank',
        'description': 'Exports of goods and services (current US$)'
    },
    'EN.ATM.CO2E.PC': {
        'source': 'World Bank',
        'description': 'CO2 emissions per capita (metric tons)'
    },
    'EN.ATM.CO2E.KT': {
        'source': 'World Bank',
        'description': 'CO2 emissions (kt)'
    },
    'SL.TLF.CACT.FM.ZS': {
        'source': 'World Bank',
        'description': 'Labor force participation rate, female (% of female population ages 15+) (modeled ILO estimate)'
    },
    'SL.UEM.TOTL.ZS': {
        'source': 'World Bank',
        'description': 'Unemployment, total (% of total labor force) (modeled ILO estimate)'
    },
    'SE.PRM.NENR': {
        'source': 'World Bank',
        'description': 'School enrollment, primary (% net)'
    },
    'IT.NET.BBND.P2': {
        'source': 'World Bank',
        'description': 'Fixed broadband subscriptions (per 100 people)'
    },
    'IT.CEL.SETS.P2': {
        'source': 'World Bank',
        'description': 'Mobile cellular subscriptions (per 100 people)'
    },
    'SH.H2O.SAFE.ZS': {
        'source': 'World Bank',
        'description': 'Improved water source (% of population with access)'
    },
    'SH.STA.ACSN': {
        'source': 'World Bank',
        'description': 'Improved sanitation facilities (% of population with access)'
    },
    'SH.DYN.MORT': {
        'source': 'World Bank',
        'description': 'Mortality rate, under-5 (per 1,000 live births)'
    },
    'FP.CPI.TOTL.ZG': {
        'source': 'World Bank',
        'description': 'Inflation, consumer prices (annual %)'
    },
    'BN.CAB.XOKA.CD': {
        'source': 'World Bank',
        'description': 'Current account balance (BoP, current US$)'
    },
    'NE.EXP.GNFS.CD': {
        'source': 'World Bank',
        'description': 'Exports of goods and services (BoP, current US$)'
    },
    'NE.IMP.GNFS.CD': {
        'source': 'World Bank',
        'description': 'Imports of goods and services (BoP, current US$)'
    },
    'NE.TRD.GNFS.CD': {
        'source': 'World Bank',
        'description': 'Trade in goods and services (BoP, current US$)'
    },
    'DT.DOD.DECT.CD': {
        'source': 'World Bank',
        'description': 'External debt stocks, total (DOD, current US$)'
    },
    'FI.RES.TOTL.CD': {
        'source': 'World Bank',
        'description': 'Total reserves (includes gold, current US$)'
    },
    'GC.DOD.TOTL.CN': {
        'source': 'World Bank',
        'description': 'Central government debt, total (current LCU)'
    }
}

CACHE_DIR = './cache'

def get_indicator(indicator_code, group_code):
    indicator = indicators.get(indicator_code)
    if indicator is not None:
        if indicator['source'] == 'World Bank':
            return get_world_bank_data(indicator_code, group_code)
        else:
            return None
    else:
        print("Indicator not found in list.")
        return None

def download_indicators_data(group_code):
    for indicator_code in indicators:
        get_indicator(indicator_code, group_code)

def get_world_bank_data(indicator_code, group_code):
    group = [country_code for country_code in get_group_countries_iso3(group_code)]
    countries = ';'.join(group) 
    indicator = indicators.get(indicator_code)
    print(indicator_code)
    if indicator is not None:
        cache_file = os.path.join(CACHE_DIR, f"{indicator_code}_{group_code}.json")  # Modify cache file name based on indicator code and group
        if os.path.exists(cache_file):
            # Check if the cache file is older than a month
            cache_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(cache_file))
            current_time = datetime.datetime.now()
            if (current_time - cache_modified_time).days <= 30:
                # Read the data from the cache file
                with open(cache_file, 'r') as file:
                    data = json.load(file)
                print("Data found in cache. Returning data.")
                return data
    
        # Fetch data from the World Bank API for group countries only
        url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator_code}?date=2010:2023&per_page=10000&format=json"
        print("Request sent to %s" % url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print("Data fetched from the World Bank API.")
            # Check if there are more pages of data
            if 'pages' in data[0] and data[0]['pages'] > 1:
                pages = data[0]['pages']
                print("fetching data from %d pages" % pages)
                if pages > 1:
                    # Fetch data from all pages
                    for page in range(2, pages + 1):
                        url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator_code}?date=2010:2023&format=json&per_page=10000&page={page}"
                        response = requests.get(url)
                        if response.status_code == 200:
                            page_data = response.json()
                            data[1].extend(page_data[1])
                        else:
                            print(f"Failed to fetch data from page {page} of the World Bank API.")
            # Save the data to the cache file
            print("Saving data to cache file.")
            with open(cache_file, 'w') as file:
                json.dump(data, file)
            return data
        else:
            print("Data saved to cache file. Returning data.")
            return None

def download_all_indicators(group_code):
    for indicator_code in indicators:
        sleep(20) # Sleep for 20 seconds between requests to avoid hitting the API rate limit
        get_indicator(indicator_code, group_code)

def load_indicator_country_data_from_cache(indicator_code, group_code, country_name):
    cache_file = os.path.join(CACHE_DIR, f"{indicator_code}_{group_code}.json")
    country_data = []
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as file:
            data = json.load(file)
            for item in data[1]:
                if item['country']['value'] == country_name:
                    country_data.append(item)
            return country_data
    
    return None