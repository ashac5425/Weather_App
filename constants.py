import os 
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

API_KEY =os.getenv("API_KEY")

import requests

from constants import BASE_URL, API_KEY

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return None, response.status_code, response.text

    data = response.json()
    if data.get("cod") != 200:
        return None, 404, f"City '{city}' not found"

    result = {
        "city": data.get("name", "Unknown City"),
        "temperature": data["main"].get("temp", "N/A"),
        "humidity": data["main"].get("humidity", "N/A"),
        "wind": data["wind"].get("speed", "N/A")
    }

    return result, 200, "Success"