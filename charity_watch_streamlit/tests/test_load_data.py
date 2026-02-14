import pytest
from charity_watch_streamlit.services.load_data import load_charities, load_geojson, load_imd

def test_load_charities_invalid_path_suffix_error_expected():
    dummy_path = 'somethin/data.jsonnn'
    with pytest.raises(ValueError):
        load_charities(dummy_path)

def test_load_charities_path_does_not_exist_raised_error_expected():
    dummy_path = 'somethin/data.jsonnn'
    with pytest.raises(ValueError):
        load_charities(dummy_path)

def test_load_geojson_invalid_file_type_error_expected():
    dummy_path = 'somethin/data.json'
    with pytest.raises(ValueError):
        load_geojson(dummy_path)

def test_load_geojson_path_does_not_exist_raised_error_expected():
    dummy_path = 'somethin/data.jsonnn'
    with pytest.raises(ValueError):
        load_geojson(dummy_path)

def test_load_imd_invalid_file_type_error_expected():
    dummy_path = 'somethin/data.geojson'
    with pytest.raises(ValueError):
        load_imd(dummy_path)

def test_load_imd_path_does_not_exist_raised_error_expected():
    dummy_path = 'somethin/data.jsonnn'
    with pytest.raises(ValueError):
        load_imd(dummy_path)