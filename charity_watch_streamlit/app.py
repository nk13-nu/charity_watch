#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import plotly.express as px
import pydeck as pdk

#importing services



def main():
    st.set_page_config(page_title="Charity Watch", layout='wide', initial_sidebar_state='collapsed')
    background_image = 'charity_watch_streamlit/resources/tower_hamlets_image.jpg'

    st.title("Charity Watch")

    st.text_input("X", placeholder="X")

if __name__ == "__main__":
    main()