import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# Function to fetch the country name using reverse geocoding
def get_country_name(lat, lon):
    try:
        # Nominatim API URL for reverse geocoding
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json&addressdetails=1"
        response = requests.get(url)
        data = response.json()

        # Extract the country name if available
        if 'address' in data and 'country' in data['address']:
            return data['address']['country']
        else:
            return "Country not found"
    except Exception as e:
        return f"Error: {e}"

# Initialize session state for map, markers, and clicked location
if 'map' not in st.session_state:
    st.session_state.map = folium.Map(location=[40.7128, -74.0060], zoom_start=5)

if 'markers' not in st.session_state:
    st.session_state.markers = []

if 'last_click' not in st.session_state:
    st.session_state.last_click = None

# Create a container for information so we can replace it
info_container = st.empty()

# Display the map and catch click events
st.title("Interactive Map with Streamlit")
st.write("Click on the map to add a marker and get coordinates.")

# Display the current map and capture the click event
clicked_location = st_folium(st.session_state.map, width=725)

# If the user clicks, show and update the information, while preserving previous data
if clicked_location and 'last_clicked' in clicked_location:
    lat = clicked_location['last_clicked']['lat']
    lon = clicked_location['last_clicked']['lng']

    # Get the country name using reverse geocoding
    country = get_country_name(lat, lon)

    # Store the country and the last clicked location in session state for persistent access
    st.session_state.last_click = (lat, lon, country)

    # Add new marker to the list of markers (preserve all markers)
    st.session_state.markers.append((lat, lon, country))

    # Add the new marker to the map (do not reset the map)
    folium.Marker([lat, lon], popup=f"New Marker at ({lat}, {lon}) in {country}").add_to(st.session_state.map)

# Add all stored markers to the map
for marker in st.session_state.markers:
    folium.Marker([marker[0], marker[1]], popup=f"Marker at ({marker[0]}, {marker[1]}) in {marker[2]}").add_to(st.session_state.map)

# Re-render the map with all markers, maintaining previous state
st_folium(st.session_state.map, width=725)

# Update the information below the map based on the last clicked location
if st.session_state.last_click:
    lat, lon, country = st.session_state.last_click
    info_container.write(f"You clicked at Latitude: {lat}, Longitude: {lon}")
    info_container.write(f"The country is: {country}")
else:
    info_container.write("Click on the map to get coordinates and country information.")
