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

#importing services/methods
from charity_watch_streamlit.services.load_data import (load_charities as _load_charities, 
                                                        load_geojson as _load_geojson, 
                                                        load_imd as _load_imd)

st.set_page_config(page_title="Charity Watch", layout='wide', initial_sidebar_state='collapsed')


###############################################
################ LOADING DATA #################
###############################################

@st.cache_data
def load_charities(path: str):
    return _load_charities(path)

@st.cache_data
def load_geojson(path: str):
    return _load_geojson(path)

@st.cache_data
def load_imd(path: str):
    return _load_imd(path)

df = load_charities("data/charities_with_deprivation.json")
lsoa_geo = load_geojson("data/lsoa_clean.geojson")
lsoa_imd = load_imd("data/lsoa_to_imd_mapping.json")

###############################################
###############################################

print(df.head())