import pytest
from charity_watch_streamlit.services.load_data import load_data

def test_load_data_invalid_path_suffix_error_expected():
    dummy_path = 'somethin/data.jsonnn'
    with pytest.raises(ValueError):
        load_data(dummy_path)

def test_load_data_path_does_not_exist_raised_error_expected():
    dummy_path = 'somethin/data.json'
    with pytest.raises(FileNotFoundError):
        load_data(dummy_path)