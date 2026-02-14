#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pydeck as pdk
from streamlit_extras.metric_cards import style_metric_cards
from pathlib import Path

#importing services
from charity_watch_streamlit.services.load_data import load_data
from charity_watch_streamlit.services.geogson_to_imd_lookup import enrich_geojson_with_imd

st.set_page_config(page_title="Charity Watch", layout='wide', initial_sidebar_state='collapsed')
background_image = 'charity_watch_streamlit/resources/tower_hamlets_image.jpg'

#Setting main title
st.title("Charity Watch")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Charities", "299")

with col2:
    st.metric("IMD", "9.4")

with col3:
    st.metric("X", "42")