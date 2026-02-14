import folium
import pandas as pd
from typing import Dict, Any, Callable, Set


def build_map(df: pd.DataFrame, lsoa_geo: Dict[str, Any],lsoa_imd: Dict[str, Any], gap_codes: Set[str], deprivation_colour: Callable, app_colour_palette: Dict[str, str],) -> folium.Map:
    """DOCSTRING HEREEEEEE"""
    #first we create a folium map object centred in Tower Hamlets, using darkmatter for nice style and zoom at 13
    m = folium.Map(location=[51.52, -0.04], zoom_start=13, tiles="cartodbdark_matter", scrollWheelZoom=False)

    #now we group the charity dataframe by LSOA code, counting how many charities are in each lsoa and adding their income
    charity_counts = df.groupby("lsoaCode").agg(
        count=("id", "count"),
        total_income=("income", "sum"),
    )

    #now we turn charity counts into a dictionary where each key is an lsoa code and the values are the aggregated columns
    charity_counts = charity_counts.to_dict("index")

    #for each polygon within the lsoa geojson
    for feature in lsoa_geo["features"]:
        #get the lsoa code
        code = feature["properties"]["LSOA21CD"]
        #use the code to retrieve the imd score from the lsoa imd file
        imd = lsoa_imd.get(code, {})
        #use the code to get the number of charities in that lsoa from the charity_counts dictionary
        stats = charity_counts.get(code)
        #using the imd variable we get the imd score for that lsoa
        score = imd.get("imdScore")
        #and with the same imd variable we get the name for the lsoa instead of using the code
        name = imd.get("name", code)
        #if the count in stats is not null we get the 
        count = stats["count"] if stats else 0
        is_gap = code in gap_codes

        folium.GeoJson(
            feature,
            style_function=lambda x, c=deprivation_colour(score), gap=is_gap: {
                "fillColor": "#f87171" if gap else c,
                "fillOpacity": 0.55 if gap else 0.35,
                "color": "#f87171" if gap else app_colour_palette["border"],
                "weight": 2.5 if gap else 1,
                "dashArray": "6 4" if gap else "0",
            },
            tooltip=(
                f"{'⚠️ ' if is_gap else ''}"
                f"<b>{name}</b> · IMD: {score} · {count} charities"
                f"{' · COMMISSIONING GAP' if is_gap else ''}"
            ),
        ).add_to(m)

