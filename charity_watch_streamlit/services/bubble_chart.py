import plotly.express as px
import pandas as pd

def build_bubble_chart(df:pd.DataFrame, charities_in_lsoa = None) -> px.scatter:
    """

    """
    
    bubble_scatter = df.groupby("primaryFocus").agg(avg_income=("income", "mean"), avg_imd=("imdScore", "mean"), count=("id", "count")).reset_index()
    bubble_scatter = bubble_scatter[bubble_scatter["count"] >= 2]

    #if charities in lsoa has data and there are charities in that lsoa
    if charities_in_lsoa is not None and len(charities_in_lsoa) > 0:
        #check the primary focus of all charities in the lsoa using a set to drop multiple instances
        clicked_focuses = set(charities_in_lsoa["primaryFocus"].dropna())
        #creating a new column in the dataframe to highlight all focuses that appear
        bubble_scatter["highlighted"] = bubble_scatter["primaryFocus"].isin(clicked_focuses)
    else:
        bubble_scatter["highlighted"] = False

    #now we create the figure with plotly express with hover data nicely formatted
    fig = px.scatter(bubble_scatter,x="avg_income",y="avg_imd", size="count", hover_name="primaryFocus", color="highlighted",
        hover_data={"avg_income": ":,.0f", "avg_imd": ":.1f", "count": True, "highlighted": False},size_max=35,
    )
    return fig