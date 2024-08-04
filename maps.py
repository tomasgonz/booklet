import streamlit as st
import folium

# Function to convert DMS to decimal degrees
def dms_to_decimal(degrees, minutes, direction):
    decimal = degrees + minutes / 60
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

# Function to parse DMS string and convert to decimal degrees
def parse_dms(dms_str):
    try:
        # Remove any commas and split the string into parts
        dms_str = dms_str.replace(',', '')
        dms_parts = dms_str.split()
        
        # Parse latitude
        lat_degrees = int(dms_parts[0])
        lat_minutes = int(dms_parts[1])
        lat_direction = dms_parts[2]
        
        # Parse longitude
        lon_degrees = int(dms_parts[3])
        lon_minutes = int(dms_parts[4])
        lon_direction = dms_parts[5]
        
        # Convert to decimal
        lat = dms_to_decimal(lat_degrees, lat_minutes, lat_direction)
        lon = dms_to_decimal(lon_degrees, lon_minutes, lon_direction)
        return lat, lon
    except Exception as e:
        st.error(f"Error parsing DMS string: {e}")
        return None, None

# Function to create a Folium map based on DMS coordinates
def create_map_from_dms(dms_str):
    lat, lon = parse_dms(dms_str)
    if lat is None or lon is None:
        st.error("Invalid coordinates, cannot create map.")
        return None
    
    country_map = folium.Map(location=[lat, lon], zoom_start=5)
    folium.Marker([lat, lon], popup=f"{dms_str}").add_to(country_map)
    
    return country_map