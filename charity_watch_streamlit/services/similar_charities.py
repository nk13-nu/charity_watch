import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_similarity_matrix(df: pd.DataFrame):
    """
    calculates and returns the cosine similarity matrix of a tfidf matrix of charity aims and activities
    """
    #first we take the aim and activities of each charity, join them and standardise them
    text = (df["aim"].fillna("") + " " + df["activities"].fillna("")).str.lower()
    #now we initialise the vectoriser 
    tfidf = TfidfVectorizer(max_features=200, stop_words="english", min_df=2, max_df=0.8)
    #we use the vectoriser object to transform each piece of text and create a matrix of vectorised charities
    X = tfidf.fit_transform(text)
    #now we calculate the cosine similarity for the matrix
    cosine_sim = cosine_similarity(X)
    #and return it
    return cosine_sim


def get_similar_charities(df: pd.DataFrame, sim_matrix, charity_id: int, n: int = 3) -> pd.DataFrame:
    """
    This function takes a dataframe, the cosine similarity matrix and a charity id, to find the most similar charities
    to the given charity based on the calculated cosine similarity of the TF-IFD vectors from the conjoined
    aims and activities text.
    """
    #first we define a dataframe for the given charity id
    charity_index = df.index[df["id"] == charity_id]
    #this is important to handle errors. If the charity id is not in the dataframe we simply return the dataframe
    #and continute running
    if len(charity_index) == 0:
        return pd.DataFrame()

    #we take the row position of the charity of interest
    idx = charity_index[0]
    #and take all of the similarity scores between this charity and all other charities
    scores = list(enumerate(sim_matrix[idx]))
    #finally we sort the scores to then filter in the next step
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    #now we take the top scores, we need to importantnly skip the first one (which is itself)
    most_similar_charities = []
    for i, j in scores[1: n+1]:
        most_similar_charities.append(i)

    #finally we select those top three charities using iloc and we take their name, focus, income and lsoa code
    result = df.iloc[most_similar_charities][["name", "primaryFocus", "income", "lsoaCode"]].copy()
    #we then add the similarity values for those top close charities
    result["similarity"] = [scores[j+1][1] for j in range(n)]
    #and finally we format the similarity as a percentage by chaining formatting columns and adding a string to show % match
    result["similarity"] = (result["similarity"] * 100).round(0).astype(int).astype(str) + "% match"

    return result