#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import pydeck as pdk
from pathlib import Path

#importing custom style
from charity_watch_streamlit.style.style import app_style_design, APP_COLOUR_PALETTE

#importing services/methods
from charity_watch_streamlit.services.load_data import (load_charities as _load_charities, 
                                                        load_lsoa_gdf as _load_lsoa_gdf, 
                                                        load_imd as _load_imd)
from charity_watch_streamlit.services.statistics_and_helpers import identify_comissioning_gaps, deprivation_colour
from charity_watch_streamlit.services.map import build_map
from charity_watch_streamlit.services.bubble_chart import build_bubble_chart

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
def load_lsoa_gdf(lsoa_df_path:str, imd_path: str, charities_path:str):
    return _load_lsoa_gdf(lsoa_df_path, imd_path, charities_path)

@st.cache_data
def load_imd(path: str):
    return _load_imd(path)

#now we load data 
df = load_charities("data/charities_with_deprivation.json")
lsoa_gdf = _load_lsoa_gdf("data/lsoa_clean.geojson", "data/lsoa_to_imd_mapping.json", "data/charities_with_deprivation.json")
lsoa_imd = load_imd("data/lsoa_to_imd_mapping.json")

@st.cache_data
def get_gap_codes():
    """"""
    return set(lsoa_gdf[lsoa_gdf["is_gap"]]["LSOA21CD"])

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





