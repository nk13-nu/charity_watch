from charity_watch_streamlit.services.helpers import deprivation_colour, identify_comissioning_gaps, income_formatting
import pytest


### Tests for deprivation colour
def test_deprivation_colour_no_deprivation_returns_none():
    result = deprivation_colour(None)
    assert result == None

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(40)
    assert result == "#d70f0f"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(32)
    assert result == "#d23b3b"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(25)
    assert result == "#fd700b"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(20)
    assert result == "#f5b905"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(15)
    assert result == "#7cc70d"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(8)
    assert result == "#22c55e"


### Tests for identify_comissioning gaps
def test_identify_comissioning_gaps_returns_dictionary():
    pass


def test_income_formatting_returns_str():
    income = 33000
    result = income_formatting(income)
    assert isinstance(result, str)


def test_retrieve_lsoa_specific_data_from_click_returns_str():
    pass

def test_retrieve_lsoa_specific_data_from_click_returns_None():
    pass
