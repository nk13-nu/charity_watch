from charity_watch_streamlit.services.helpers import deprivation_colour, identify_comissioning_gaps


### Tests for deprivation colour
def test_deprivation_colour_no_deprivation_returns_none():
    result = deprivation_colour(None)
    assert result == None

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(40)
    assert result == "#dc2626"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(32)
    assert result == "#ef4444"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(25)
    assert result == "#f97316"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(20)
    assert result == "#eab308"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(15)
    assert result == "#84cc16"

def test_deprivation_colour_high_deprivation_returns_red_colour():
    result = deprivation_colour(8)
    assert result == "#22c55e"


### Tests for identify_comissioning gaps
