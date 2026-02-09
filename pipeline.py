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

#Finally we export the final dataframe as a csv file into the data directory
final_df.to_csv('data/charities_with_deprivation.csv', index=False)