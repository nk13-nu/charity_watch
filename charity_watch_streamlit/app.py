#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import plotly.express as px
from pathlib import Path

#Setting global page configurations
st.set_page_config(page_title="Charity Watch", layout='Wide', initial_sidebar_state='expanded')

def load_data(file_path_json :str) -> pd.DataFrame:
    path = Path(file_path_json)
    if path.suffix.lower() != '.json' or path.suffix.lower() != 'geojson':
        raise ValueError("File must be either json or geojson")
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    if path.suffix.lower() == 'json':
        df = pd.read_json("data/charities_with_deprivation.json")
    if path.suffix.lower() == 'geojson':
        pass
    return df

