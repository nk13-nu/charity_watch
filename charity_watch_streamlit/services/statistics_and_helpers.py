#FUNCTIONS TO CALCULATE STATISTICS AND HELPERS
import pandas as pd #pandas for data manipulation
from typing import Any #any from typing for data typing

def deprivation_colour(deprivation_score : float | int) -> str:
    """A function that returns a stoplight palette of colours for deprivation data"""
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


def identify_comissioning_gaps(df: pd.DataFrame, lsoa_geo:dict[str, Any], lsoa_imd : dict[str,dict[str, Any]]) -> list[dict[str, Any]]:
    """This function identifies LSOA's with high deprivation scores but no charity coverage"""
    #first we create a set of all LSOA's that have at least one charity
    lsoa_covered = set(df["lsoaCode"].dropna().unique())
    #we instantiate an empty list to store all lsoas without charities
    commissioning_gaps = []

    #for each feature in the features column of the lsoa geojson we
    for feature in lsoa_geo["features"]:
        #extract the lsoa code for that feautre
        lsoa_code = feature["properties"]["LSOA21CD"]
        #extract the imd score for the lsoa code that we just extracted
        imd = lsoa_imd.get(lsoa_code, {})
        #and we then get the imd decile of that specific imd
        decile = imd.get("imdDecile")
        #then we run some validation which if passed we append ...
        if lsoa_code not in lsoa_covered and decile is not None and decile <= 3:
            #we append the lsoa code, name, the imd score for that lsoa, its decile and population
            commissioning_gaps.append({
                "code": lsoa_code,
                "name": imd.get("name", lsoa_code),
                "imdScore": imd.get("imdScore", 0),
                "imdDecile": decile,
                "population": imd.get("population", 0),
            })
    #finally we return the comissioning gaps list which includes a dictionary of lsoa's with the extracted data.
    return commissioning_gaps


