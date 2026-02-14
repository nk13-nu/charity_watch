import pandas as pd
from pathlib import Path
from typing import Any
import json
import streamlit as st
import geopandas as gpd
    

def load_charities(file_path: str) -> pd.DataFrame:
    #we convert into path object for easier access
    path = Path(file_path)
    #if the path does not contain .json we raise a value error
    if path.suffix.lower() != ".json":
        raise ValueError("File must be json")
    #if the path does not exist we raise and error
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    #if the path is a json file we read with pandas
    if path.suffix.lower() == ".json":
        return pd.read_json(path)


# def load_geojson(file_path:str) -> dict[str, Any]:
    #we convert into path object for easier access
#    path = Path(file_path)
     #if the path does not contain .geojson we raise a value error
#    if path.suffix.lower() != ".geojson":
        raise ValueError("File must be geojson")
    #if the path does not exist we raise and error
#    if not path.exists():
        raise FileNotFoundError("File not found at path")
    #if the path is a geojson file we read with json
#    if path.suffix.lower() == ".geojson":
#        with open(file_path) as f:
#           return json.load(f)
   
def load_imd(file_path : str) -> dict[str, Any]:
    path = Path(file_path)
     #if the path does not contain .json we raise a value error
    if path.suffix.lower() != ".json":
        raise ValueError("File must be json")
    #if the path does not exist we raise and error
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    #if the path is a json file we read with json
    if path.suffix.lower() == ".json":
        with open(file_path) as f:
            return json.load(f)

def load_lsoa_gdf(geojson_path: str) -> gpd.GeoDataFrame:
    geojson_path = Path(geojson_path)
    if not geojson_path.exists():
        raise FileNotFoundError(f"GeoJSON file not found: {geojson_path}")
    gdf = gpd.read_file(geojson_path)
    
    #To make this a complete dataset we need to merge the imd dataset with the gpd
    #so we call the method defined above
    imd = load_imd()
    #we create a dataframe of deprivation data
    imd_df = (pd.DataFrame.from_dict(imd, orient="index").rename_axis("LSOA21CD").reset_index())
    #and we merge the imd_df with the geopandas dataframe on the column 'LSOA21CD' which is the LSOA for TH
    gdf = gdf.merge(imd_df, on="LSOA21CD", how="left")
    
    #now we load all charities using the function defined above
    charities = load_charities()
    #we calculate charity statistics with a groupby, grouping by lsoa, counting charities by lsoa and calculating total income
    charity_stats = (charities.groupby("lsoaCode").agg(charity_count=("id", "count"),total_income=("income", "sum"),).reset_index().rename(columns={"lsoaCode": "LSOA21CD"}))
    #and just as with imd we merge with the geopandas dataframe on lsoacode 
    gdf = gdf.merge(charity_stats, on="LSOA21CD", how="left")

    #now we deal with possible null values resulting from aggregations
    gdf["charity_count"] = gdf["charity_count"].fillna(0).astype(int)
    gdf["total_income"] = gdf["total_income"].fillna(0)

    #finally we create a new column called is_gap to find if there is a comissioning gap in the lsoa
    #we do this by checking if there are no charities in the lsoa, there is an imd decile and it is less than or equal to 3
    #which means that there is a deprived neighbourhood without local charities
    gdf["is_gap"] = ((gdf["charity_count"] == 0) & (gdf["imdDecile"].notna()) & (gdf["imdDecile"] <= 3))
    return gdf
 
    