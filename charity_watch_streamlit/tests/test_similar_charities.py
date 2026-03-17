from charity_watch_streamlit.services.load_data import load_charities
from charity_watch_streamlit.services.similar_charities import build_similarity_matrix, get_similar_charities

data_path = "data/charities_with_deprivation.json"

#first we test that the cosine similarity matrix is indeed square with one row and one column per charity
def test_similarity_matrix_shape():
    df = load_charities(data_path)
    test = build_similarity_matrix(df)
    assert test.shape == (len(df), len(df))

#check the get similar charities function from the built matrix does return the wanted number of charities
def test_returns_two_results():
    df = load_charities(data_path)
    test = build_similarity_matrix(df)
    results = get_similar_charities(df, test, charity_id =df.iloc[0]["id"], n=2)
    assert len(results) == 2

#now we check that a charity never appears in its own returned similar charities list
def test_excludes_itself():
    df = load_charities(data_path)
    test = build_similarity_matrix(df)
    first = df.iloc[0]
    results = get_similar_charities(df, test, charity_id= first["id"], n=3)
    assert first["name"] not in results["name"].values

#finally we test that a non existent charity id returns an empty dataframe
def test_invalid_id_returns_empty():
    df = load_charities(data_path)
    test = build_similarity_matrix(df)
    results = get_similar_charities(df, test, charity_id= 23948, n=3)
    assert results.empty