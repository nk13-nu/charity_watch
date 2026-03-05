#FUNCTIONS TO CALCULATE STATISTICS AND HELPERS
import pandas as pd #pandas for data manipulation
import geopandas as gpd #geopandas for geojson and geo pandas dataframe manipulation
from typing import Any, Dict, List #any from typing for data typing
from shapely.geometry import Point #to create point vectors out of coordinates

def deprivation_colour(deprivation_score : float | int) -> str:
    """
    A function that returns a stoplight palette of colours for deprivation data

    Args:
        - deprivation_score (int or float): the deprivation score
    Returns:
        - string: the hex value of the corresponding colour to the deprivation score
    """
    #if the deprivation score is none we return none
    if deprivation_score is None:
        return None
    #if the deprivation score is greater than 40, that is a very high a depriavtion score, we return the hex of a bright red
    if deprivation_score >= 40:
        return "#dc2626"
    #if the deprivation score is greater than 30, that is a high a depriavtion score, we return the hex of a red
    if deprivation_score >= 30:
        return "#ef4444"
    #if the deprivation score is greater than 24, that is a medium a deprivation score, we return the hex of orange
    if deprivation_score >= 24:
         return "#f97316"
    #if the deprivation score is greater than 20, that is a low mid depriavtion score, we return the hex of yellow
    if deprivation_score >= 20:
        return "#eab308"
    #if deprivation score is greater than or equal to 15 the function returns a lime colour
    if deprivation_score >= 15:
        return "#84cc16"
    #else we return a bright green for everything less than 15.
    return "#22c55e"


def identify_comissioning_gaps(lsoa_gdf: gpd.GeoDataFrame) -> List[Dict]:
    """
    Returns a dictionary of all lsoas that have been identified as having gaps between deprivation and local charities
    
    Args:
        - lsoa_gdf (gpd.GeoDataFrame): the geodataframe containing all lsoas, their shapes, and imd data
    Returns:
        - list: a list of dictionaries with keys corresponding to relevant columns of the lsoa in comissioning gap position
    """
    # 
    gap_rows = lsoa_gdf[lsoa_gdf["is_gap"]]
    return gap_rows[["LSOA21CD", "name", "imdScore", "imdDecile", "population"]].rename(columns={"LSOA21CD": "code"}).to_dict("records")


def income_formatting(income_value:float | int) -> str:
    """
    Formats income value for display so that it looks better and is more readable
    Args:
        - income_value(float or int): the income of the charity or the total income to format
    Returns:
        - str: formatted income
    """
    #if the income is greater than 1 million we divide by 1 million and add an M for readability
    if income_value >= 1_000_000:
        return f"£{income_value / 1_000_000:.1f}M"
    #if the income is greater than or equal to 1 thousand we divide by 1000 and add the K
    if income_value >= 1_000:
        return f"£{income_value / 1_000:.0f}K"
    #we return the formatted income as a string with £.
    return f"£{income_value:,.0f}"

def retrieve_lsoa_specific_data_from_click(lsoa_gdf: gpd.GeoDataFrame, lsoa_map_click:Dict) -> str | None:
    """
    When the user clicks on one of the lsoa areas within the folium map, folium returns a dictionary of coordinates.
    This function takes that dictionary of coordinates and the main geopandas dataframe and searches within the dataframe
    to find if any of the lsoa polygons within the dataframe contains that point, if it does it returns the LSOA code for 
    the polygon (that contains the point).
    
    Args:
        - lsoa_gdf (gpd.GeoDataframe): the main geopandas dataframe
        - lsoa_map_clicks (Dictionary): a dictionary that folium returns everytime there is a click in the map

    Returns:
        - str : a string of the lsoa code if it was found that the point was within it
        - None: if there is no clicked data or there is no match between polygon area and point
    """
    #if there is no map click return None
    if not lsoa_map_click:
        return None
    #when there is a click we create a shapely point using the longitude and latitude returned by Folium
    point_clicked = Point(lsoa_map_click['lng'], lsoa_map_click['lat'])
    #we check if the lsoa_gdf contains the point object, the point clicked.
    match = lsoa_gdf[lsoa_gdf.contains(point_clicked)]
    #if there is a match, that is, match is a geodf with at least one row
    if len(match) > 0:
        #we return the lsoa code of that polygon
        return match.iloc[0]['LSOA21CD']
    #else we return none
    return None

def process_financial_history(api_json_response: List[Dict]) -> pd.DataFrame:
    """
    Gets the response in JSON from the api and converts it into a dataframe.
    """
    #we define an empty list to parse the api data which will store dictionaries
    financial_data = []
        
    #for every available record 
    for i in api_json_response:
            #we first extract the year and take only the year leaving the month and day behind
            year = i["financial_period_end_date"][:4]
            #then we take the income, if it is contained else we append 0
            income = i["income"] or 0
            #now we take the charity's expenditure
            expenditure = i["expenditure"] or 0
            #and finally we take the government grants
            government_grants = i["income_from_govt_grants"] or 0
            
            #now we append the whole record (for that specific year) into the list 
            financial_data.append({
                "Year": int(year),
                "Income": income,
                "Expenditure": expenditure,
                "Govt Grants": government_grants
            })
            
    #and we convert the list into a dataframe 
    df = pd.DataFrame(financial_data)
        
    #finally we sort the values by year to make sure that the plotting works correclty and do a bit of defensive programming
    if not df.empty:
         df.sort_values(by="Year", inplace=True)

    return df