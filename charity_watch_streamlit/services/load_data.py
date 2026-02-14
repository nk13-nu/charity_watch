#
# A simple function to load json files
#

import pandas as pd
from pathlib import Path
import geopandas as gpd

#Method to load JSON data as well as geoJSON data
def load_data(file_path_json: str) -> pd.DataFrame:
    path = Path(file_path_json)
    if path.suffix.lower() not in {".json", ".geojson"}:
        raise ValueError("File must be either json or geojson")
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    if path.suffix.lower() == ".json":
        return pd.read_json(path)
    if path.suffix.lower() == ".geojson":
        return gpd.read_file(path)