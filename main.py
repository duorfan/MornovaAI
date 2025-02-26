from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from src.ai.assistant import suggest_wake_up_time
from src.api.google_calendar import get_calendar_events
from src.api.weather_api import get_weather_forecast
from src.api.spotify import get_spotify_recommendations

# Load environment variables
load_dotenv()

app = Flask(__name__)

### 🔹 API Endpoints ###

@app.route("/wake-up-time", methods=["GET"])
def wake_up_time():
    """Returns AI-generated wake-up time suggestion."""
    return jsonify({"wake_up_time": suggest_wake_up_time()})

@app.route("/calendar", methods=["GET"])
def calendar():
    """Fetches upcoming Google Calendar events."""
    return jsonify({"events": get_calendar_events()})

@app.route("/weather", methods=["GET"])
def weather():
    """Fetches weather forecast data."""
    return jsonify(get_weather_forecast())

@app.route("/spotify", methods=["GET"])
def spotify():
    """Fetches AI-generated Spotify music recommendations."""
    return jsonify(get_spotify_recommendations())

@app.route("/", methods=["GET"])
def home():
    """Simple status check route."""
    return jsonify({"message": "Mornova AI backend is running!"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))  # Use PORT from .env or default to 5001
    app.run(debug=True, host="0.0.0.0", port=port)
