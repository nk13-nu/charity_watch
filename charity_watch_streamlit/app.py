#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import plotly.express as px

#Setting global page configurations
st.set_page_config(page_title="Charity Watch", layout='Wide', initial_sidebar_state='expanded')

#Importing dataset
df = pd.read_json("data/charities_with_deprivation.json")

