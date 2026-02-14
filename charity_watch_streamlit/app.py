#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import plotly.express as px

#importing services
from charity_watch_streamlit.services.load_data import load_data



def main():
    st.set_page_config(page_title="Charity Watch", layout='wide', initial_sidebar_state='expanded')





if __name__ == "__main__":
    main()