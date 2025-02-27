import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("Missing WEATHER_API_KEY. Check your .env file!")

def get_weather_forecast():
    """Fetches and filters weather data for Mornova AI"""
    location = "New York"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days=1"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        # Extract useful information
        current_weather = data.get("current", {})
        forecast = data.get("forecast", {}).get("forecastday", [{}])[0]
        
        filtered_data = {
            "date": forecast.get("date"),
            "feelslike_c": current_weather.get("feelslike_c"),
            "condition": current_weather.get("condition", {}).get("text"),
            "daily_chance_of_rain": forecast.get("day", {}).get("daily_chance_of_rain", 0),
            "is_day": current_weather.get("is_day")
        }

        return filtered_data
    else:
        return {"error": f"Failed to fetch weather data. Status code: {response.status_code}"}

# ✅ Add this so it prints when running the file directly
if __name__ == "__main__":
    print(get_weather_forecast())
