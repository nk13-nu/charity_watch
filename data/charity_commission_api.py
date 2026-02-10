import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("CCEW_API_KEY")
org_number = 211536

r = requests.get(f"https://api.charitycommission.gov.uk/register/api/charityFinancialHistory/{org_number}/0",headers={"Ocp-Apim-Subscription-Key": API_KEY})
print(r.status_code)
print(r.json())