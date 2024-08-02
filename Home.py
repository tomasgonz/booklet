import streamlit as st
import pandas as pd
from indicators import indicators, load_indicator_country_data_from_cache
from groups import get_group_countries_name, get_iso3_from_name, get_name_from_iso3, get_fips_from_iso3, get_iso2_from_name
from country_facts import load_country_data, load_factbook_data, country_small_flags, get_small_flag

#group_name = st.sidebar.selectbox("Select the group of countries", ["LDCs", "LLDCs", "SIDS"])
group_name = "LLDCs"
# Load the codes and descriptions to be used in this app
data = {}
for code in indicators:
    data[code] = {'source': indicators[code]['source'], 'description': indicators[code]['description']}

# Create a sidebar panel with the names of all the countries in the group to display specific data on them
group = get_group_countries_name(group_name.lower())
group.sort()

selected_country = st.sidebar.selectbox("Select Country", group)

st.sidebar.markdown(f"# List of {group_name}")

for country in group:
    iso3 = get_iso3_from_name(country, "lldcs")
    flag = get_small_flag(iso3)
    st.sidebar.markdown(f"{flag} {country}")   

def normalize_dictionary(data):
    # Normalize the nested dictionary data
    df = pd.json_normalize(data)
    # Flattening specific columns
    df = df.rename(columns={
        'indicator.id': 'indicator_id',
        'indicator.value': 'indicator_value',
        'country.id': 'country_id',
        'country.value': 'country_value'})
    
    # Remove rows with None values in the 'date' column
    df = df.dropna(subset=['value'])
    
    return df

def display_chart(data, title, source):
    # Load the data for the selected country
    if data is not None:
        with st.container(border=True):
            st.text(title)
            df = normalize_dictionary(data)
            if not df.empty:
                latest_value = df.loc[df['date'].idxmax(), 'value'].round(2)
                latest_year = df.loc[df['date'].idxmax(), 'date']
                first_value = df.loc[df['date'].idxmin(), 'value'].round(2)
                first_year = df.loc[df['date'].idxmin(), 'date']

                cola, colb = st.columns([1, 1])
                with cola:
                    st.metric(label=first_year, value=first_value)
                with colb:
                    delta_value = (((latest_value - first_value) / first_value)*100).round(2)
                    st.metric(label=latest_year, value=latest_value, delta=delta_value)
                
                st.line_chart(df, x ='date', y='value', x_label='Date', y_label='Value')
                
                st.caption(f"Source: {source}")     
            else:
                st.write("No series data available for this country")

if selected_country:
    selected_country_iso2 = get_iso2_from_name(selected_country)
    selected_country_iso3 = get_iso3_from_name(selected_country, group_name.lower())
    selected_country_fips = get_fips_from_iso3(selected_country_iso3)

    country_data = load_country_data(selected_country_iso3)
    factbook_data = load_factbook_data(selected_country_fips)
    st.title(f" {selected_country}")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
            st.subheader("Environment")

            st.markdown(f"**Climate**<br>{factbook_data['Environment']['Climate']['text']}", unsafe_allow_html=True)

            # Load the data for the selected country
            indicator_data = load_indicator_country_data_from_cache("EN.ATM.CO2E.KT", group_name.lower(), selected_country)
            display_chart(indicator_data, "CO2 emissions ((kt))", "World Bank")
            
            #st.markdown(f"**Current environmental issues**<br>{factbook_data['Environment']['Environment - current issues']['text']}", unsafe_allow_html=True)

            st.markdown(f"**Party to the following environmental international agreements**<br>{factbook_data['Environment']['Environment - international agreements']['party to']['text']}", unsafe_allow_html=True)

            # Load the data for the selected country
            indicator_data = load_indicator_country_data_from_cache("EN.ATM.CO2E.PC", group_name.lower(), selected_country)
            display_chart(indicator_data, "CO2 emissions (pc)", "World Bank")

            st.subheader("Labor force")
            
            st.markdown(f"**Youth unemployment rate**<br>{factbook_data['Economy']['Youth unemployment rate (ages 15-24)']['total']['text']}", unsafe_allow_html=True)

            # Load the data for the selected country
            indicator_data = load_indicator_country_data_from_cache("SL.TLF.CACT.FM.ZS", group_name.lower(), selected_country)
            display_chart(indicator_data, "Labor force participation rate for ages 15-24 (% of population)", "World Bank")

            st.markdown(f"**Unemployment rate**<br>{factbook_data['Economy']['Unemployment rate']['Unemployment rate 2023']['text']}", unsafe_allow_html=True)
            
            # Load the data for the selected country
            indicator_data = load_indicator_country_data_from_cache("SL.UEM.TOTL.ZS", group_name.lower(), selected_country)
            display_chart(indicator_data, "Unemployment, total (% of total labor force)", "World Bank")

            st.subheader("Population")

            if 'Population distribution' in factbook_data['People and Society']:
                
                st.markdown(f"**Population**<br>{factbook_data['People and Society']['Population distribution']['text']}", unsafe_allow_html=True)
            
            indicator_data = load_indicator_country_data_from_cache("SP.POP.TOTL", group_name.lower(), selected_country)
            display_chart(indicator_data, "Population, total", "World Bank")

            st.subheader("Education")
            
            st.markdown(f"**Education expenditure**<br>{factbook_data['People and Society']['Education expenditures']['text']}", unsafe_allow_html=True)

            # Load the data for the selected country
            indicator_data = load_indicator_country_data_from_cache("SE.PRM.NENR", group_name.lower(), selected_country)
            display_chart(indicator_data, "Net enrollment rate, primary (% of primary school age children)", "World Bank")

            st.subheader("Connectivity")
            st.markdown(f"**% connected to internet**<br>{factbook_data['Communications']['Internet users']['percent of population']['text']}", unsafe_allow_html=True)

            st.markdown(f"**% connected to fixed broadband**<br>{factbook_data['Communications']['Broadband - fixed subscriptions']['subscriptions per 100 inhabitants']['text']}", unsafe_allow_html=True)

            # Load the data for the selected country
            indicator_data = load_indicator_country_data_from_cache("IT.NET.BBND.P2", group_name.lower(), selected_country)
            display_chart(indicator_data, "Fixed broadband subscriptions (per 100 people)", "World Bank")   

            st.subheader("Economy")
            st.markdown(f"**Main manufactured products**<br>{factbook_data['Economy']['Industries']['text']}", unsafe_allow_html=True)

            st.markdown(f"**Main agricultural products**<br>{factbook_data['Economy']['Agricultural products']['text']}", unsafe_allow_html=True)

            st.markdown(f"##### Macroecoonomic indicators", unsafe_allow_html=True)

            indicator_data = load_indicator_country_data_from_cache("NY.GDP.MKTP.PP.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "GDP (current US$)", "World Bank")

            indicator_data = load_indicator_country_data_from_cache("NY.GDP.PCAP.PP.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "GDP per capita (current US$)", "World Bank")

            indicator_data = load_indicator_country_data_from_cache("FP.CPI.TOTL.ZG", group_name.lower(), selected_country)
            display_chart(indicator_data, "Inflation, consumer prices (annual %)", "World Bank")

            st.markdown(f"##### Trade", unsafe_allow_html=True)

            indicator_data = load_indicator_country_data_from_cache("BN.CAB.XOKA.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "Current account balance (current US$)", "World Bank")

            indicator_data = load_indicator_country_data_from_cache("NE.EXP.GNFS.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "Exports of goods and services (current US$)", "World Bank")

            indicator_data = load_indicator_country_data_from_cache("NE.IMP.GNFS.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "Imports of goods and services (current US$)", "World Bank")

            st.markdown(f"##### Debt and reserves", unsafe_allow_html=True)

            indicator_data = load_indicator_country_data_from_cache("DT.DOD.DECT.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "External debt (current US$)", "World Bank")

            indicator_data = load_indicator_country_data_from_cache("FI.RES.TOTL.CD", group_name.lower(), selected_country)
            display_chart(indicator_data, "Total reserves (includes gold, current US$)", "World Bank")

            indicator_data = load_indicator_country_data_from_cache("GC.DOD.TOTL.CN", group_name.lower(), selected_country)
            display_chart(indicator_data, "Central government debt, total (current LCU)", "World Bank")
        
    with col2:
        st.image(f"https://flagcdn.com/w320/{selected_country_iso2.lower()}.png")
        st.image(f"./cache/maps/{selected_country_iso2.lower()}_256.png")
        st.markdown(f"**Official name**<br> {country_data[0]['name']['official']}", unsafe_allow_html=True)
        if (country_data[0]['demonyms']):
                st.markdown(f"**Demonym**<br> {country_data[0]['demonyms']['eng']['m']}", unsafe_allow_html=True)
        st.markdown(f"**Translation**<br>\
                    {country_data[0]['name']['official']}\
                    {country_data[0]['translations']['ara']['official']}<br>\
                    {country_data[0]['translations']['zho']['official']}<br>\
                            {country_data[0]['translations']['fra']['official']}<br>\
                                {country_data[0]['translations']['rus']['official']}<br>\
                                    {country_data[0]['translations']['spa']['official']}", unsafe_allow_html=True)

        st.markdown(f"**Capital**<br> {country_data[0]['capital'][0]}", unsafe_allow_html=True)
        st.markdown(f"**Region**<br> {country_data[0]['region']}", unsafe_allow_html=True)
        st.markdown(f"**Subregion**<br> {country_data[0]['subregion']}", unsafe_allow_html=True)
        
        st.markdown(f"**Area**<br> {country_data[0]['area']}", unsafe_allow_html=True)
        st.markdown(f"**Population**<br> {country_data[0]['population']}", unsafe_allow_html=True)

        border_countries = [get_name_from_iso3(border) for border in country_data[0]['borders']]
        border_countries.sort()
        st.markdown(f"**Borders**<br> {', '.join(border_countries)}", unsafe_allow_html=True) 
        st.markdown(f"**Main export partners**<br>{factbook_data['Economy']['Exports - partners']['text']}", unsafe_allow_html=True)
        st.markdown(f"**Main import partners**<br>{factbook_data['Economy']['Imports - partners']['text']}", unsafe_allow_html=True)
        st.markdown(f"**Main export products**<br>{factbook_data['Economy']['Exports - commodities']['text']}", unsafe_allow_html=True)
        st.markdown(f"**Main import products**<br>{factbook_data['Economy']['Imports - commodities']['text']}", unsafe_allow_html=True)

