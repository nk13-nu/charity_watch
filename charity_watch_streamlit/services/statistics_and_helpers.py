#FUNCTIONS TO CALCULATE STATISTICS AND HELPERS
import pandas as pd #pandas for data manipulation
import geopandas as gpd #geopandas for geojson and geo pandas dataframe manipulation
from typing import Any, Dict, List #any from typing for data typing

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