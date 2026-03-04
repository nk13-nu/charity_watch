import os
import requests
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("CCEW_API_KEY")

#now we define a function to retreive financial charities financial history from the charity commission's api
def get_charity_financial_history(charity_id:int) -> dict:
    """
    Gets 5 year charity financial history from the Charity Commission API using the charity id
    """
    #set the targeted api endpoint
    url = f"https://api.charitycommission.gov.uk/register/api/charityfinancialhistory/{charity_id}/0"
    #required headers
    headers = {
        "Ocp-Apim-Subscription-Key": API_KEY,
        "Accept": "application/json"
    }
    #save the response
    response = requests.get(url, headers=headers)
    #raise for status to see if there are any errors
    response.raise_for_status()
    #and we return a json to be able to access it as a dictionary
    return response.json()