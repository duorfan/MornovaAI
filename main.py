# from flask import Flask, jsonify, render_template
# from dotenv import load_dotenv
# import os
# from datetime import datetime
# import pytz

# from src.ai.assistant import suggest_wake_up_time
# from src.api.google_calendar import get_next_events
# from src.api.weather_api import get_weather_forecast
# # from src.api.spotify import get_spotify_recommendations

# # Load environment variables

# print(suggest_wake_up_time())

# load_dotenv()

# app = Flask(__name__)

# def format_event(event):
#     """Formats event details for readability."""
#     if not event:
#         return {"message": "No upcoming events."}

#     # Convert ISO time to a readable format
#     start_time = datetime.fromisoformat(event["start"]).astimezone(pytz.timezone(event["timeZone"]))
#     end_time = datetime.fromisoformat(event["end"]).astimezone(pytz.timezone(event["timeZone"]))

#     return {
#         # "summary": event["summary"],
#         "start": start_time.strftime("%I:%M %p")
#         # "end": end_time.strftime("%I:%M %p %Z"),
#         # "location": event.get("location", "No location"),
#         # "htmlLink": event["htmlLink"]
#     }

# ### 🔹 API Endpoints ###

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route("/wake-up-time", methods=["GET"])
# def wake_up_time():
#     """Returns AI-generated wake-up time suggestion."""
#     return jsonify({"wake_up_time": suggest_wake_up_time()})

# @app.route("/calendar", methods=["GET"])
# def calendar():
#     """Fetches and returns the next 3 Google Calendar events."""
#     events = get_next_events()
#     if not events:
#         return jsonify({"message": "No upcoming events."})
#     return jsonify(events)

# @app.route("/weather", methods=["GET"])
# def weather():
#     """Fetches weather forecast data."""
#     return jsonify(get_weather_forecast())

# # @app.route("/spotify", methods=["GET"])
# # def spotify():
# #     """Fetches AI-generated Spotify music recommendations."""
# #     return jsonify(get_spotify_recommendations())

# @app.route("/", methods=["GET"])
# def home():
#     """Simple status check route."""
#     return jsonify({"message": "Mornova AI backend is running!"})

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 5001))  # Use PORT from .env or default to 5001
#     app.run(debug=True, host="0.0.0.0", port=port)

from flask import Flask, jsonify, request, render_template
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


app = Flask(__name__)

# Set your OpenAI API key from environment variables

# --- Existing Endpoints ---
# (Assuming you have endpoints for /wake-up-time, /calendar, /weather, /suggestion already implemented)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/wake-up-time", methods=["GET"])
def wake_up_time():
    # Placeholder implementation: Replace with your actual suggest_wake_up_time logic.
    from src.ai.assistant import suggest_wake_up_time  # Ensure this function is updated as needed.
    return jsonify({"wake_up_time": suggest_wake_up_time()})

@app.route("/calendar", methods=["GET"])
def calendar():
    # Assuming your get_next_events returns an array of events.
    from src.api.google_calendar import get_next_events
    events = get_next_events()
    if not events:
        return jsonify({"message": "No upcoming events."})
    return jsonify(events)

@app.route("/weather", methods=["GET"])
def weather():
    from src.api.weather_api import get_weather_forecast
    data = get_weather_forecast()
    return jsonify(data)

@app.route("/suggestion", methods=["GET"])
def suggestion():
    # Placeholder suggestion – replace with your own suggestion logic.
    return jsonify({"suggestion": "Remember to stay hydrated!"})

# --- AI Voice Assistant Endpoint ---
@app.route("/ai-assistant", methods=["POST"])
def ai_assistant():
    data = request.get_json()
    voice_input = data.get("voice_input", "")
    calendar_data = data.get("calendar", {})
    weather_data = data.get("weather", {})
    identity = data.get("identity", "")

    # Build a prompt using the provided data.
    prompt = (
        f"You are an AI assistant with the identity '{identity}'. "
        f"Here is the calendar data: {calendar_data}. "
        f"Here is the weather data: {weather_data}. "
        f"User said: {voice_input}. "
        "Please provide a helpful and concise response."
    )

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150)
        response_text = response.choices[0].message.content.strip()
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"Error contacting OpenAI: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
