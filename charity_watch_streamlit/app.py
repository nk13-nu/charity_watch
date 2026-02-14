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

#importing custom style
from charity_watch_streamlit.style.style import app_style_design, APP_COLOUR_PALETTE

#importing services/methods
from charity_watch_streamlit.services.load_data import (load_charities as _load_charities, 
                                                        load_geojson as _load_geojson, 
                                                        load_imd as _load_imd)
from charity_watch_streamlit.services.statistics_and_helpers import identify_comissioning_gaps


#Initial page configuration
st.set_page_config(page_title="Charity Watch", layout='wide', initial_sidebar_state='collapsed')


###############################################
################ LOADING DATA #################
###############################################

#we cache data for faster retrieval and create local load functions for the three datasets
@st.cache_data
def load_charities(path: str):
    return _load_charities(path)

@st.cache_data
def load_geojson(path: str):
    return _load_geojson(path)

@st.cache_data
def load_imd(path: str):
    return _load_imd(path)

#now we load data 
df = load_charities("data/charities_with_deprivation.json")
lsoa_geo = load_geojson("data/lsoa_clean.geojson")
lsoa_imd = load_imd("data/lsoa_to_imd_mapping.json")

@st.cache_data
def get_gap_codes():
    """Return the set of LSOA codes that are commissioning gaps withing Tower hamlets"""
    return {g["code"] for g in identify_comissioning_gaps()}

###############################################
################ APPLYING STYLE ###############
###############################################

st.markdown(app_style_design, unsafe_allow_html=True)

###############################################
########## ADDING WIREFRAME COMPONENTS ########
###############################################

st.markdown(
    '<h1 class="cw-title">Charity Watch</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<h5 class="cw-title">Tracking, micro, small and medium charities in Tower Hamlets</h5>',
    unsafe_allow_html=True
)

map_columns, info_columns = st.columns([5,4])

with map_columns:
    center = [51.5074, -0.1278]
    m = folium.Map(location=center, zoom_start=12, tiles="CartoDB positron")
    st_folium(m, width=1000, height=600)

