import pandas as pd
from pathlib import Path
from typing import Any
import json
import streamlit as st
    

def load_charities(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if path.suffix.lower() != ".json":
        raise ValueError("File must be json")
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    if path.suffix.lower() == ".json":
        return pd.read_json(path)


def load_geojson(file_path:str) -> dict[str, Any]:
    path = Path(file_path)
    if path.suffix.lower() != ".geojson":
        raise ValueError("File must be geojson")
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    if path.suffix.lower() == ".geojson":
        with open(file_path) as f:
            return json.load(f)
   
def load_imd(file_path : str) -> dict[str, Any]:
    path = Path(file_path)
    if path.suffix.lower() != ".json":
        raise ValueError("File must be json")
    if not path.exists():
        raise FileNotFoundError("File not found at path")
    if path.suffix.lower() == ".json":
        with open(file_path) as f:
            return json.load(f)
 
    