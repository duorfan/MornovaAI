from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

from src.ai.assistant import suggest_wake_up_time
from src.api.google_calendar import get_next_event
from src.api.weather_api import get_weather_forecast
# from src.api.spotify import get_spotify_recommendations

# Load environment variables

print(suggest_wake_up_time())

load_dotenv()

app = Flask(__name__)

def format_event(event):
    """Formats event details for readability."""
    if not event:
        return {"message": "No upcoming events."}

    # Convert ISO time to a readable format
    start_time = datetime.fromisoformat(event["start"]).astimezone(pytz.timezone(event["timeZone"]))
    end_time = datetime.fromisoformat(event["end"]).astimezone(pytz.timezone(event["timeZone"]))

    return {
        "summary": event["summary"],
        "start": start_time.strftime("%A, %b %d, %I:%M %p"),
        "end": end_time.strftime("%I:%M %p %Z"),
        "location": event.get("location", "No location"),
        "htmlLink": event["htmlLink"]
    }

### 🔹 API Endpoints ###

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/wake-up-time", methods=["GET"])
def wake_up_time():
    """Returns AI-generated wake-up time suggestion."""
    return jsonify({"wake_up_time": suggest_wake_up_time()})

@app.route("/calendar", methods=["GET"])
def calendar():
    """Fetches and formats the next Google Calendar event."""
    next_event = get_next_event()
    formatted_event = format_event(next_event)
    return jsonify({"event": formatted_event})

@app.route("/weather", methods=["GET"])
def weather():
    """Fetches weather forecast data."""
    return jsonify(get_weather_forecast())

# @app.route("/spotify", methods=["GET"])
# def spotify():
#     """Fetches AI-generated Spotify music recommendations."""
#     return jsonify(get_spotify_recommendations())

@app.route("/", methods=["GET"])
def home():
    """Simple status check route."""
    return jsonify({"message": "Mornova AI backend is running!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))  # Use PORT from .env or default to 5001
    app.run(debug=True, host="0.0.0.0", port=port)

