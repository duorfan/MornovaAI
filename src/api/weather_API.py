import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_weather_data():
    """Fetches weather data from an API"""
    api_key = os.getenv("WEATHER_API_KEY")  # Load from .env
    location = "New York"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1"

    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
