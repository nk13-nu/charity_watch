#This code was AI generated to quickly convert a csv file into json
import csv
import json

csv_file_path = '../data/charities_with_deprivation.csv'
json_file_path = '../data/charities_with_deprivation.json'

data = []

# Read CSV
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Write JSON
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Converted {csv_file_path} to {json_file_path}")