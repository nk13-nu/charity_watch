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
from charity_watch_streamlit.services.helpers import identify_comissioning_gaps, deprivation_colour, retrieve_lsoa_specific_data_from_click
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

#dividing the app into 9 columns, five for the map and the rest for the data cards that appear after an lsoa is clicked
map_columns, info_columns = st.columns([5,4])

#using the map columns we build the map using the build map method
with map_columns:
    folium_map = build_map(lsoa_gdf, deprivation_colour=deprivation_colour)
    charity_map_data = st_folium(folium_map, width=None, height=650)

#we constantly check the map for clicks and when we get one the method defined in the helper module gets called, giving us data for that lsoa
clicked_lsoa = retrieve_lsoa_specific_data_from_click(lsoa_gdf, charity_map_data.get("last_clicked") if charity_map_data else None)

#using the 4 info columns
with info_columns:
    #if clicked lsoa contains data (that is only after the user clicked on an lsoa on the map)
    if clicked_lsoa:
        #retrieve all data for the clicked lsoa
        imd_info = lsoa_imd.get(clicked_lsoa, {})

        #now we store values individually for display
        #we store lsoa name
        lsoa_name = imd_info.get("name", clicked_lsoa)
        #the lsoa's imd score
        score = imd_info.get("imdScore", "—")
        #storing the population of the lsoa
        population = imd_info.get("population", "—")
        #and the number of charities within the lsoa as a dataframe (to include multiple fields of the charity)
        charities_here = df[df["lsoaCode"] == clicked_lsoa]

        #displaying some data for testing
        st.text(lsoa_name)
        st.text(score)
        st.text(population)