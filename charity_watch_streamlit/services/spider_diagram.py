import plotly.graph_objects as go

#We first create a mapping for each column name that will appear in the chart
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
    """
    Gets all deprivation level ratings per lsoa
    """
    #getting each imd column name contained as keys
    imd_column_names = list(imd_categories_breakdown.keys())
    #we remove all duplicate lsoas and create a list of lsoa code and imd columns
    lsoa_imd_scores = df.drop_duplicates(subset="lsoaCode")[["lsoaCode"] + imd_column_names].copy()
    #for each imd in the categories breakdown defined above
    for i, j in imd_categories_breakdown.items():
        #we take all imd scores at that specific lsoa and create a new column which contains the rank *100
        lsoa_imd_scores[f"{i}_percentage"] = lsoa_imd_scores[i].rank(pct=True) * 100

    #we then define an empty dictionary
    lsoa_imd_dict = {}
    #we loop through each lsoa ignoring the index
    for _, j in lsoa_imd_scores.iterrows():
        #extract the lsoa code
        lsoa_code = j["lsoaCode"]
        #then use a dictionary comprehension to extract the percentage for that imd and round its value getting a dictionary with the key as an lsoa
        #code and the items as a dictionary of the lsoa's imd scores
        lsoa_imd_dict[lsoa_code] = {label: round(j[f"{i}_percentage"], 1) for i, label in imd_categories_breakdown.items()}
    return lsoa_imd_dict

def build_spider_chart(lsoa_code, df):
    """
    Build a radial chart for the lsoa breakdown
    """
    #first we retrieve all the imd ranking for that Losa using the function defined above
    lsoa_ranks = get_imd_rankings_per_lsoa(df).get(lsoa_code)
    
    if not lsoa_ranks:
        return None

    #we then extract all of the lsoa's imd names
    lsoas = list(lsoa_ranks.keys())
    #we then take the scores
    imd_scores = list(lsoa_ranks.values())
    #and append the first value again to return to loop back
    lsoas.append(lsoas[0])
    imd_scores.append(imd_scores[0])

    #now we define the figure
    fig = go.Figure()
    #we update the layout and add a title, we also add the polar parameter to set a standard range between all charts
    fig.update_layout(title = dict(text = 'Selected LSOA Deprivation Breakdown'), polar=dict(
        radialaxis=dict( visible=True, 
                        range=[0, 100], 
                        tickvals=[0, 25, 50, 75, 100],
                        ticktext=["0", "25", "50", "75", "100"],
                        tickfont=dict(color="black"))
        ),
        showlegend=False)


    #and we add the trace using Scatterpolar
    fig.add_trace(go.Scatterpolar(
    r = imd_scores, #the radius will be defined by the imd scores
    theta =lsoas, #the angle by the imd names
    fill ="toself", #to get a solid polygon
    fillcolor ="rgba(29, 86, 193, 0.15)", #we add the fill colour
    line =dict(color="#1d56c1", width=2), #and change the colour and width of the line
    name =f"{lsoa_code}", #we also add the legend label making it the selected lsoa code
    hovertemplate="%{theta}: %{r:.0f}th percentile<extra></extra>",)) #and adjust the tooltip


    return fig
