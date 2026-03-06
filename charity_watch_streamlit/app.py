#Imports
import streamlit as st #streamlit for the app
import pandas as pd #pandas for data manipulation
import json #json to work with json files
import folium
from streamlit_folium import st_folium
import pydeck as pdk
from pathlib import Path
from streamlit_extras.stylable_container import stylable_container #using streamlit extras to style cards with ease (https://medium.com/snowflake/style-and-customize-your-streamlit-in-snowflake-apps-4a8495b8e469)

#importing custom style
from charity_watch_streamlit.style.style import app_style_design, APP_COLOUR_PALETTE, statistic_cards_style, statistic_cards_small_style, bottom_cards_style, click_an_lsoa_on_map_style

#importing services/methods
from charity_watch_streamlit.services.load_data import (load_charities as _load_charities, 
                                                        load_lsoa_gdf as _load_lsoa_gdf, 
                                                        load_imd as _load_imd)

from charity_watch_streamlit.services.helpers import (identify_comissioning_gaps, 
                                                      deprivation_colour, 
                                                      retrieve_lsoa_specific_data_from_click, 
                                                      income_formatting)

from charity_watch_streamlit.services.map import build_map
from charity_watch_streamlit.services.bubble_chart import build_bubble_chart
from charity_watch_streamlit.services.spider_diagram import build_spider_chart

from streamlit_extras.metric_cards import style_metric_cards

from services.api_line_chart import build_charity_income_line_chart
from services.helpers import process_financial_history
from services.load_api_data import get_charity_financial_history

#Initial page configuration
st.set_page_config(page_title="Charity Watch", layout='wide', initial_sidebar_state='collapsed')

#for the charity selection this is important, it checks if there has been a charity selected for the first run of the code
#if there is no seleciton then we set the selection state to none
if "selected_charity" not in st.session_state:
    st.session_state.selected_charity = None


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


imd_categories_breakdown = {
    "incomeScore":"Income",
    "employmentRate":'Employement',
    "educationSkillsTrainingScore": "Education",
    "healthDeprivation":"Health",
    "crimeDeprivation" :"Crime",
    "housingBarriersDeprivation":"Housing",
    "livingEnvScore":"Living Environment",
}

@st.cache_data
def get_imd_rankings_per_lsoa(df):
    imd_column_names = list(imd_categories_breakdown.keys())
    lsoa_imd_scores = df.drop_duplicates(subset="lsoaCode")[["lsoaCode"] + imd_column_names].copy()
    for i, j in imd_categories_breakdown.items():
        lsoa_imd_scores[f"{i}_percentage"] = lsoa_imd_scores[i].rank(pct=True) * 100

    lsoa_imd_dict = {}
    for _, j in lsoa_imd_scores.iterrows():
        lsoa_code = j["lsoaCode"]
        lsoa_imd_dict[lsoa_code] = {
            label: round(j[f"{i}_percentage"], 1) for i, label in imd_categories_breakdown.items()}
    return lsoa_imd_dict



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

#The Info columns are triggered only when there has been an lsoa click
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
        score = imd_info.get("imdScore", "No imd score to show")
        #storing the population of the lsoa
        population = imd_info.get("population", "No population count registered")
        #and the number of charities within the lsoa as a dataframe (to include multiple fields of the charity)
        charities_here = df[df["lsoaCode"] == clicked_lsoa]

        #displaying some data for testing
        #https://medium.com/snowflake/style-and-customize-your-streamlit-in-snowflake-apps-4a8495b8e469
        with stylable_container('LSOA Name Card', css_styles=statistic_cards_style):
                st.markdown(f"""<div 
                                style="
                                font-size: 32px;
                                font-weight: 700;
                                color: #E8F5E9;
                                letter-spacing: -0.5px;">
                                {lsoa_name}
                            </div>""",
                            unsafe_allow_html=True)

        #if there are charities to in the lsoa, then
        if len(charities_here) > 0:
            #for every charity, we ignore the index and take c as the iterator to create a button for each
            for _, c in charities_here.iterrows():
                #we retrieve the id
                charity_id = c["id"]
                # and we create a button for the charity that will include the name, and a key to identify it based on the charity id
                if st.button(f"{c['name']}", key=f"charity_{charity_id}", use_container_width=True):
                    st.session_state.selected_charity = charity_id

            spider_figure = build_spider_chart(clicked_lsoa, df)
            if spider_figure:
                st.plotly_chart(spider_figure, use_container_width=True, key="radar_selected")

            bubble_figure = build_bubble_chart(df, charities_here)
            st.plotly_chart(bubble_figure, use_container_width=True, key="bubble_selected")
        #If there are no charities in the lsoa we check for a commissionnig gap
        else:
            #if the clicked lsoa code is in the get_gap_codes dictionary (large imd score and no charities)
            is_gap = clicked_lsoa in get_gap_codes()
            #we say that there is a comissioning gap
            if is_gap:
                st.text('Commissioning Gap!!!')
            else:
                #if there is not commissioning gap we just say that there are no charities registered at that lsoa
                st.text('No Charities Registered')

#if an lsoa is clicked on the map
if clicked_lsoa:
    #we retrieve all imd information
    imd_info = lsoa_imd.get(clicked_lsoa, {})
    #get the lsoa name
    lsoa_name = imd_info.get("name", clicked_lsoa)
    #and all data about charities within the lsoa
    charities_here = df[df["lsoaCode"] == clicked_lsoa]

    #display text signaling which lsoa is selected
    st.text(f'Showing: {lsoa_name}')

    #set 4 columns
    c1, c2, c3, c4 = st.columns(4)
    #on column 1 we place number of charities in lsoa
    with c1:
        with stylable_container('Number of Charities', css_styles=bottom_cards_style):
                st.markdown(f"""<div 
                                style="
                                font-size: 22px;
                                font-weight: 500;
                                color: #E8F5E9;
                                letter-spacing: -0.5px;">
                                {f"Number of Charities: {len(charities_here)}"}
                            </div>""",
                            unsafe_allow_html=True)
    #column 2 takes the total income of the lsoa's charities
    with c2:
        with stylable_container('Total Last Recorded Income', css_styles=bottom_cards_style):
                st.markdown(f"""<div 
                                style="
                                font-size: 22px;
                                font-weight: 500;
                                color: #E8F5E9;
                                letter-spacing: -0.5px;">
                                {f"Total Last Recorded Income: {income_formatting(charities_here["income"].sum())}"}
                            </div>""",
                            unsafe_allow_html=True)
    #column3 we pass the deprivation score of the lsoa
    with c3:
        with stylable_container('Deprivation Score', css_styles=bottom_cards_style):
                st.markdown(f"""<div 
                                style="
                                font-size: 22px;
                                font-weight: 500;
                                color: #E8F5E9;
                                letter-spacing: -0.5px;">
                                {f"Deprivation Score: {imd_info.get("imdScore", "No deprivation score registered")}"}
                            </div>""",
                            unsafe_allow_html=True)
    #column 4 for the population
    with c4:
        with stylable_container('Population LSOA', css_styles=bottom_cards_style):
                st.markdown(f"""<div 
                                style="
                                font-size: 22px;
                                font-weight: 500;
                                color: #E8F5E9;
                                letter-spacing: -0.5px;">
                                {f"Population: {imd_info.get("population", 0):,}"}
                            </div>""",
                            unsafe_allow_html=True)
else:
    #if there is no selected lsoa on the map we go back to defaults
    c1, c2, c3, c4 = st.columns(4)
    #ww first display the total number of (small, medium, micro) charities in the dataset/tower hamlets
    with c1:
        st.text(f"Number of Charities: {len(df)}")
    #calculate avergae last recorded income across borough and display it
    with c2:
        st.text(f"Average Last Recorded Income: {income_formatting(df["income"].mean())}")
    #calculate average deprivation score 
    with c3:
        st.text(f"Average Deprivation Score {df["imdScore"].mean()}")
    #and display the lsoa charity coverage across tower hamlets
    with c4:
        st.text(f"LSOA Charity Coverage {df["lsoaCode"].nunique()}/{len(df)}")
    with info_columns:
         with stylable_container('Click an LSOA Card', css_styles=click_an_lsoa_on_map_style):
              st.markdown(f"""<div 
                                style="
                                font-size: 22px;
                                text-align: center;
                                font-weight: 500;
                                color: #E8F5E9;
                                letter-spacing: -0.5px;">
                                {"Click an LSOA on the Map to see all charity information."}
                            </div>""",
                            unsafe_allow_html=True)

#if a charity button is clicked
if st.session_state.selected_charity is not None:
    # we now filter for the clicked (button) in the dataframe
    charity_row = df[df["id"] == st.session_state.selected_charity]
    #if we get a charity
    if len(charity_row) > 0:
        #we now create a pandas series using iloc for that specific charitys
        charity = charity_row.iloc[0]
        #using the st.dialog decorator creates a popup window for the charity
        @st.dialog(f"{charity['name']}", width="large")
        #the following function renders the popup window
        def show_charity_popup_window():
            #firs there will be a single row with three columns for key charity stats and facts
            column1, column2, column3 = st.columns(3)
            with column1:
                st.text(f"Last Recorded Income: {income_formatting(charity['income'])} ")
            with column2:
                st.text(f"Last Recorded Expenditure: {income_formatting(charity['expenditure'])}")
            with column3:
                st.text(f"Size: {charity['sizeBand']}")
            
            #Then we add text for the charity number, aim and Location
            st.text(f"Charity Number: {charity['id']}")
            st.text(f"Aim: {charity.get("aim", "No aim registered")}")
            st.text(f'Location: {charity.get("address", "No Address Registered")}, {charity.get("postcode", "")}')

            #creating two columns for the streetview and the financial data api chart
            streetview_col, financial_data_col = st.columns(2)
            #on the streetview column we add the streetview pane
            with streetview_col:
                if pd.notna(charity.get("lat")) and pd.notna(charity.get("lng")):
                    #we render a markdown window with streetview
                    st.markdown(f"""
                    <div class="cw-streetview" style="margin-top:16px;  display:flex; justify-content:left;">
                        <iframe
                            width="100%" height="350" frameborder="0" loading="lazy"
                            src="https://www.google.com/maps/embed/v1/streetview?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&location={charity["lat"]},{charity["lng"]}&heading=210&pitch=10&fov=75">
                        </iframe>
                    </div>
                    """, unsafe_allow_html=True)
            #and on the financial data line chart column we call the defined functions to:
            with financial_data_col:
                 #create a dataframe by calling the api using the selected charity's id and then processing the data into a df
                 financial_hist_df = process_financial_history(get_charity_financial_history(charity_id= charity['id']))
                 #and then passing that df into the line chart builder function
                 build_charity_income_line_chart(charity['name'], financial_hist_df)

            st.markdown("<br>", unsafe_allow_html=True)

        #we call the method to create the popup window for the charity
        show_charity_popup_window()
        #then we reset the state back to None so that the app does not keep the popup open
        st.session_state.selected_charity = None