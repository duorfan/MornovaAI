import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from src.api.google_calendar import get_calendar_events
from src.api.weather_api import get_weather_forecast
from openai import OpenAI

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def suggest_wake_up_time():
    """AI logic to determine an optimal wake-up time based on calendar and weather."""
    events = get_calendar_events()
    weather = get_weather_forecast()

    # Find earliest event
    earliest_event = min(events, key=lambda e: e["start_time"]) if events else None

    if not earliest_event:
        return "No events scheduled. Wake up at your preferred time!"

    wake_up_time = datetime.strptime(earliest_event["start_time"], "%Y-%m-%dT%H:%M:%S") - timedelta(hours=1)

    # Adjust based on weather conditions
    if "rain" in weather["forecast"]:
        wake_up_time -= timedelta(minutes=15)  # Wake up earlier if it's raining.

    # Use GPT to refine the suggestion
    prompt = f"""
    Given that the earliest event is at {earliest_event["start_time"]} and the weather is {weather["forecast"]}, 
    what is a good wake-up time to ensure I'm ready while maximizing sleep?
    """
    response = client.Completion.create(model="gpt-4", prompt=prompt, max_tokens=50)
    ai_suggestion = response["choices"][0]["text"].strip()

    return ai_suggestion or wake_up_time.strftime("%H:%M:%S")

__all__ = ["suggest_wake_up_time"]
