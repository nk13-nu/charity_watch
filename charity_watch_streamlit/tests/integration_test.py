from charity_watch_streamlit.services.load_data import load_charities, load_imd, load_lsoa_gdf
from charity_watch_streamlit.services.similar_charities import build_similarity_matrix, get_similar_charities
from charity_watch_streamlit.services.helpers import identify_comissioning_gaps
from charity_watch_streamlit.services.spider_diagram import get_imd_rankings_per_lsoa

#defining variables of file paths
data_path = "data/charities_with_deprivation.json"
geo_json_file = "data/lsoa_clean.geojson"
imd_file = "data/lsoa_to_imd_mapping.json"


# Integration test to test load charities function
def test_charities_load():
    df = load_charities(data_path)
    assert not df.empty
    assert "name" in df.columns
    assert "lsoaCode" in df.columns
    assert "imdScore" in df.columns


#Integration test to test load_lsoa_gdf to check if the geodataframe does build with imd and charity counts merged
def test_lsoa_gdf_loads():
    gdf = load_lsoa_gdf(geo_json_file, imd_file, data_path)
    assert len(gdf) > 0
    assert "imdScore" in gdf.columns
    assert "charity_count" in gdf.columns
    assert "is_gap" in gdf.columns


#integration test to check if the imd file loads and matches charity LSOA codes
def test_imd_matches_charities():
    df = load_charities(data_path)
    imd = load_imd(imd_file)
    charity_codes = set(df["lsoaCode"].dropna().unique())
    missing = charity_codes - set(imd.keys())
    assert len(missing) == 0


#testing if the similar charities function does return only three valid results
def test_similar_charities():
    df = load_charities(data_path)
    sim = build_similarity_matrix(df)
    sample_id = df.iloc[0]["id"]
    results = get_similar_charities(df, sim, sample_id, n=3)
    assert len(results) == 3
    assert "similarity" in results.columns
    for val in results["similarity"]:
        assert val.endswith("% match")


#testing for the key functionality of commissioning gaps appearing only in LSOAs with no charities
def test_commissioning_gaps():
    gdf = load_lsoa_gdf(geo_json_file, imd_file, data_path)
    gaps = identify_comissioning_gaps(gdf)
    for gap in gaps:
        row = gdf[gdf["LSOA21CD"] == gap["code"]]
        assert row.iloc[0]["charity_count"] == 0

#final check to see if all lsoa imd ranking are present, that relevant fields are contained
def test_spider_rankings():
    df = load_charities(data_path)
    rankings = get_imd_rankings_per_lsoa(df)
    assert len(rankings) > 0
    first_lsoa = list(rankings.values())[0]
    assert "Income" in first_lsoa
    assert "Health" in first_lsoa