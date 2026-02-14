import folium
import pandas as pd
import geopandas as gpd
from typing import Dict, Any, Callable, Set
from charity_watch_streamlit.services.helpers import deprivation_colour
from charity_watch_streamlit.style.style import APP_COLOUR_PALETTE



def build_map(lsoa_gdf: gpd.GeoDataFrame, deprivation_colour: Callable) -> folium.Map:
    """"""
    #first we create a folium map object centred in Tower Hamlets, using darkmatter for nice style and zoom at 13
    m = folium.Map(location=[51.52, -0.04], zoom_start=13, tiles="cartodbdark_matter", scrollWheelZoom=False)

    #now we loop through every row of the iterrows return, skipping the index and getting:
    for _, row in lsoa_gdf.iterrows():
        #we first get the imdscore and store it in the score variable
        score = row.get("imdScore")
        #we now get the name of the lsoa
        name = row.get("name", row["LSOA21CD"])
        #now we store the number of charities at that (row/lsoa)
        count = row["charity_count"]
        #and we store the is there a gap variable
        is_gap = row["is_gap"]

        #now we create using geojson each polygon or division in the map
        folium.GeoJson(
            #since for each row in the dataframe we have a geometry, we need to convert that geometry into geojson format
            row.geometry.__geo_interface__,
            #then here we define the map colouring, c tells us the deprivation colour (from styles) and the gap is whether there is a commissioning gap
            #the idea of this lambda function is to colour each LSOA respective to its imd and highlight those with gaps
            #this is fundamental for the map and the app
            style_function=lambda x, c=deprivation_colour(score), gap=is_gap: {
                #if there is a comissioning gap in the lsoa we colour it in red else in the respective deprivation colour defined in styles
                "fillColor": "#f87171" if gap else c,
                #the opacity is also dependent on the gap, if there is a gap we colour stronger
                "fillOpacity": 0.55 if gap else 0.35,
                #same as fillcolor, for the borded
                "color": "#f87171" if gap else APP_COLOUR_PALETTE["border"],
                #lsoa's with gap get higher weight
                "weight": 2.5 if gap else 1,
                #if there is a gap the border is also dashed
                "dashArray": "6 4" if gap else "0",
            },
            #now we define the tooltip text whose texts also depends on whether there is a comissioning gap or not
            tooltip=f"{' ATTENTION! ' if is_gap else ''}<b>{name}</b> · IMD: {score} · {count} charities{' · COMMISSIONING GAP' if is_gap else ''}",
        ).add_to(m) #and add it to the map

    return m #finally we return the map obj