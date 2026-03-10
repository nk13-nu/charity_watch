import plotly.graph_objects as go

imd_categories_breakdown = {
    "incomeScore":"Income",
    "employmentRate":'Employement',
    "educationSkillsTrainingScore": "Education",
    "healthDeprivation":"Health",
    "crimeDeprivation" :"Crime",
    "housingBarriersDeprivation":"Housing",
    "livingEnvScore":"Living Environment",
}

def get_imd_rankings_per_lsoa(df):
    imd_column_names = list(imd_categories_breakdown.keys())
    lsoa_imd_scores = df.drop_duplicates(subset="lsoaCode")[["lsoaCode"] + imd_column_names].copy()
    for i, j in imd_categories_breakdown.items():
        lsoa_imd_scores[f"{i}_percentage"] = lsoa_imd_scores[i].rank(pct=True) * 100

    lsoa_imd_dict = {}
    for _, j in lsoa_imd_scores.iterrows():
        lsoa_code = j["lsoaCode"]
        lsoa_imd_dict[lsoa_code] = {
            label: round(j[f"{i}_percentage"], 1) for i, label in imd_categories_breakdown.items()}
    return lsoa_imd_dict

def build_spider_chart(lsoa_code, df):
    lsoa_ranks = get_imd_rankings_per_lsoa(df).get(lsoa_code)
    
    if not lsoa_ranks:
        return None

    lsoas = list(lsoa_ranks.keys())
    imd_scores = list(lsoa_ranks.values())
    lsoas.append(lsoas[0])
    imd_scores.append(imd_scores[0])

    fig = go.Figure()

    fig.update_layout(title = dict(text = 'Selected LSOA Deprivation Breakdown'), polar=dict(
        radialaxis=dict( visible=True, 
                        range=[0, 100], 
                        tickvals=[0, 25, 50, 75, 100],
                        ticktext=["0", "25", "50", "75", "100"])
        ),
        showlegend=False)


    fig.add_trace(go.Scatterpolar(
    r = imd_scores,
    theta =lsoas,
    fill ="toself",
    fillcolor ="rgba(29, 86, 193, 0.15)",
    line =dict(color="#1d56c1", width=2),
    name =f"{lsoa_code}",
    hovertemplate="%{theta}: %{r:.0f}th percentile<extra></extra>",))


    return fig