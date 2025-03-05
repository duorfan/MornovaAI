from datetime import datetime, timedelta
import sys
import os
import importlib

# Ensure the script runs correctly as a module
if "src.ai.assistant" in sys.modules:
    importlib.reload(sys.modules["src.ai.assistant"])

# Ensure the 'src' package is correctly located
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.api.google_calendar import get_next_events
from src.api.weather_api import get_weather_forecast

def suggest_wake_up_time():
    """Determine an optimal wake-up time based on calendar and weather."""
    events = get_next_events()  # Now returns a list of events
    if not events or len(events) == 0:
        return "No events scheduled. Wake up at your preferred time!"
    
    # Use the first event in the list.
    event = events[0]

    try:
        # Extract event time from the dictionary.
        event_time_str = event.get("start")  # Adjusted to match your printed structure
        event_time = datetime.strptime(event_time_str, "%Y-%m-%dT%H:%M:%S%z")
    except Exception as e:
        return f"Error parsing event time: {e}"

    # Set default wake-up time (1 hour before the event)
    wake_up_time = event_time - timedelta(hours=1)

    # Get weather forecast
    try:
        weather = get_weather_forecast()
        if weather and "forecast" in weather and isinstance(weather["forecast"], str):
            if "rain" in weather["forecast"].lower():
                wake_up_time -= timedelta(minutes=15)
    except Exception as e:
        return f"Error fetching weather data: {e}"

    return wake_up_time.strftime("%H:%M:%S")
