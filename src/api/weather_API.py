import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("Missing WEATHER_API_KEY. Check your .env file!")

def get_weather_forecast():
    """Fetches weather data from an API"""
    location = "New York"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=1"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch weather data. Status code: {response.status_code}"}

# ✅ Add this so it prints when running the file directly
if __name__ == "__main__":
    print(get_weather_forecast())
