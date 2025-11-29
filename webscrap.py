from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
def ws(name):
    params = {
    "engine": "google_shopping",
    "q": name,
    "api_key": SERPAPI_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shoping_results = results["shopping_results"]
    return(shoping_results[0:5])
    