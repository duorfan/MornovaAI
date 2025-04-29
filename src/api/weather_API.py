# src/api/weather_api.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not WEATHER_API_KEY:
    raise ValueError("Missing WEATHER_API_KEY. Check your .env file!")

def get_weather_forecast():
    """Fetches and filters weather data for Mornova AI."""
    location = "Durham"
    url = (
        f"http://api.weatherapi.com/v1/forecast.json"
        f"?key={WEATHER_API_KEY}&q={location}&days=1"
    )

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch weather data. Status code: {response.status_code}"}

    data = response.json()
    current = data.get("current", {})
    forecast_day = data.get("forecast", {}).get("forecastday", [{}])[0]

    return {
        "date":                  forecast_day.get("date"),
        "temperature":           current.get("temp_c"),
        "feelslike_c":           current.get("feelslike_c"),
        "condition":             current.get("condition", {}).get("text"),
        "daily_chance_of_rain":  forecast_day.get("day", {}).get("daily_chance_of_rain", 0),
        "is_day":                current.get("is_day")
    }

if __name__ == "__main__":
    print(get_weather_forecast())
