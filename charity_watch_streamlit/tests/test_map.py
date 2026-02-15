import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from charity_watch_streamlit.services.map import build_map
import folium

def test_build_map_returns_folium_map():
    tower_hamlets_mock_data = gpd.GeoDataFrame(
        {"LSOA21CD" : ['E01000001'],
         'IMD Score': ['3.0'], 
         'Name' : ['Test'], 
         'charity_count': [10], 
         'is_gap':[False]}, geometry=[Polygon([(0,0), (0,1), (1,1), (1,0)])], crs="EPSG:4326")
    
    def deprivation_col(imd_score):
        return "#ffffff"
    
    result = build_map(tower_hamlets_mock_data, deprivation_col)
    assert isinstance(result, folium.Map)