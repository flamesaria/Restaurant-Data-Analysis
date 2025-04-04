import requests
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("YELP_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}
print("API key:", API_KEY)


url = "https://api.yelp.com/v3/businesses/search"
params = {
    "term": "restaurant",
    "location": "Warsaw",
    "limit": 50
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

restaurants = []
for biz in data["businesses"]:
    restaurants.append({
        "name": biz["name"],
        "rating": biz.get("rating"),
        "review_count": biz.get("review_count"),
        "price": biz.get("price", "N/A"),
        "category": biz["categories"][0]["title"] if biz.get("categories") else "Unknown",
        "address": biz["location"].get("address1"),
        "city": biz["location"].get("city"),
        "zip_code": biz["location"].get("zip_code"),
        "latitude": biz["coordinates"].get("latitude"),
        "longitude": biz["coordinates"].get("longitude")
    })

df = pd.DataFrame(restaurants)

df.to_csv("warsaw_restaurants.csv", index=False)
print("Data saved to 'warsaw_restaurants.csv'")