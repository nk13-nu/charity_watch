import json
import pandas as pd

df = pd.read_csv('../data/clean_data/deprivation_th.csv')

lsoa_to_imd_mapping = {}
for _, r in df.iterrows():
    lsoa_to_imd_mapping[r["LSOA code (2021)"]] = {
        "name": r["LSOA name (2021)"],
        "imdScore": round(r["Index of Multiple Deprivation (IMD) Score"], 2),
        "imdDecile": int(r["Index of Multiple Deprivation (IMD) Decile (where 1 is most deprived 10% of LSOAs)"]),
        "population": int(r["Total population: mid 2022"]),
    }

with open("lsoa_to_imd_mapping.json", "w") as f:
    json.dump(lsoa_to_imd_mapping, f, indent=2)
