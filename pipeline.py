"""
This script contains a small and simple data pipeline that ingests the clean data, standardizes postcode columns and
joins the three given datasets. The output is a csv that contains all micro, small and medium charities in 
Tower Hamlets.
"""

import pandas as pd

#first we read all csv files into dataframes
charities_df = pd.read_csv('data/clean_data/micro_small_med_charities_TH.csv')
postcodes_df = pd.read_csv('data/clean_data/post_codes_th.csv')
deprivation_df = pd.read_csv('data/clean_data/deprivation_th.csv')

#Standardizing the postcode column in both the charities and the postcodes datasets
charities_df['pc_join'] = charities_df['Charity Postcode'].str.replace(' ', '').str.upper()
postcodes_df['pc_join'] = postcodes_df['pcd'].str.replace(' ', '').str.upper()

#Now we merge charities with postcodes using merge on the common column pc_join
charities_with_postcodes = charities_df.merge(postcodes_df[['pc_join', 'lsoa21', 'lat', 'long']].drop_duplicates('pc_join'),on='pc_join', how='left')

#Now we merge the new dataset with the deprivation dataset to get IMD scores by LSOA for each charity and we merge on LSOA 2021
final_df = charities_with_postcodes.merge(deprivation_df, left_on='lsoa21', right_on='LSOA code (2021)', how='left')

#we now drop the pc_join column
final_df.drop(columns=['pc_join'], inplace=True)

#In this new step we need to drop more columns that are no longer necessary (I found this while building the app itself)
drop_cols = [
    'Unnamed: 0_x',
    'Unnamed: 0_y',
    'Phone', 'Email', 'Website',
    'Charity Constituency',
    'Charity Type',
    'TH Postcode',
    'Size Band',
    'LSOA code (2021)',
    'LSOA name (2021)',
    'Local Authority District code (2024)',
    'Local Authority District name (2024)',
    'Index of Multiple Deprivation (IMD) Rank (where 1 is most deprived)',
    'Income Rank (where 1 is most deprived)',
    'Income Decile (where 1 is most deprived 10% of LSOAs)',
    'Employment Rank (where 1 is most deprived)',
    'Employment Decile (where 1 is most deprived 10% of LSOAs)',
    'Education, Skills and Training Rank (where 1 is most deprived)',
    'Education, Skills and Training Decile (where 1 is most deprived 10% of LSOAs)',
    'Health Deprivation and Disability Rank (where 1 is most deprived)',
    'Health Deprivation and Disability Decile (where 1 is most deprived 10% of LSOAs)',
    'Crime Rank (where 1 is most deprived)',
    'Crime Decile (where 1 is most deprived 10% of LSOAs)',
    'Barriers to Housing and Services Rank (where 1 is most deprived)',
    'Barriers to Housing and Services Decile (where 1 is most deprived 10% of LSOAs)',
    'Living Environment Rank (where 1 is most deprived)',
    'Living Environment Decile (where 1 is most deprived 10% of LSOAs)',
    'Income Deprivation Affecting Children Index (IDACI) Score (rate)',
    'Income Deprivation Affecting Children Index (IDACI) Rank (where 1 is most deprived)',
    'Income Deprivation Affecting Children Index (IDACI) Decile (where 1 is most deprived 10% of LSOAs)',
    'Income Deprivation Affecting Older People (IDAOPI) Score (rate)',
    'Income Deprivation Affecting Older People (IDAOPI) Rank (where 1 is most deprived)',
    'Income Deprivation Affecting Older People (IDAOPI) Decile (where 1 is most deprived 10% of LSOAs)',
    'Children and Young People Sub-domain Score',
    'Children and Young People Sub-domain Rank (where 1 is most deprived)',
    'Children and Young People Sub-domain Decile (where 1 is most deprived 10% of LSO',
    'Adult Skills Sub-domain Score',
    'Adult Skills Sub-domain Rank (where 1 is most deprived)',
    'Adult Skills Sub-domain Decile (where 1 is most deprived 10% of LSOAs)',
    'Geographical Barriers Sub-domain Score',
    'Geographical Barriers Sub-domain Rank (where 1 is most deprived)',
    'Geographical Barriers Sub-domain Decile (where 1 is most deprived 10% of LSOAs)',
    'Wider Barriers Sub-domain Score',
    'Wider Barriers Sub-domain Rank (where 1 is most deprived)',
    'Wider Barriers Sub-domain Decile (where 1 is most deprived 10% of LSOAs)',
    'Indoors Sub-domain Score',
    'Indoors Sub-domain Rank (where 1 is most deprived)',
    'Indoors Sub-domain Decile (where 1 is most deprived 10% of LSOAs)',
    'Outdoors Sub-domain Score',
    'Outdoors Sub-domain Rank (where 1 is most deprived)',
    'Outdoors Sub-domain Decile (where 1 is most deprived 10% of LSOAs)',
    'Working age population 18-66 (for use with Employment Deprivation Domain): mid 2022'
]

final_df = final_df.drop(columns=drop_cols)

final_df = final_df.rename(columns={
    'Charity Number': 'id',
    'Charity Name': 'name',
    'Charity Address': 'address',
    'Charity Postcode': 'postcode',
    'Last Recorded Income': 'income',
    'Last Recorded Expenditure': 'expenditure',
    'How the charity helps': 'howHelps',
    'What the charity does': 'whatDoes',
    'Who the charity helps': 'whoHelps',
    'Activities': 'activities',
    'Charity Size Band': 'sizeBand',
    'Primary Focus': 'primaryFocus',
    'lsoa21': 'lsoaCode',
    'lat': 'lat',
    'long': 'lng',
    'Index of Multiple Deprivation (IMD) Score': 'imdScore',
    'Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)': 'imdDecile',
    'Income Score (rate)': 'incomeScore',
    'Employment Score (rate)': 'employmentRate',
    'Health Deprivation and Disability Score': 'healthDeprivation',
    'Crime Score': 'crimeDeprivation',
    'Barriers to Housing and Services Score': 'housingBarriersDeprivation',
    'Living Environment Score': 'livingEnvScore',
    'Total population: mid 2022': 'totalPopulation',
    'Dependent Children aged 0-15: mid 2022': 'childPopulation',
    'Older population aged 60 and over: mid 2022': 'olderPopulation',
    'Charity Objects':'aim',
    'Education, Skills and Training Score': 'educationSkillsTrainingScore',
})

#Finally we export the final dataframe as a csv file into the data directory
final_df.to_csv('data/final_data/charities_with_deprivation.csv', index=False)
#and we also need to export to json for react
final_df.to_json('data/final_data/charities_with_deprivation.json', orient='records')