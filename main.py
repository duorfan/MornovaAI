# main.py
from flask import Flask, jsonify, request, render_template
from openai import OpenAI
import os

from src.api.weather_api import get_weather_forecast

# initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# --- Existing Endpoints ---

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/wake-up-time", methods=["GET"])
def wake_up_time():
    from src.ai.assistant import suggest_wake_up_time
    return jsonify({"wake_up_time": suggest_wake_up_time()})

@app.route("/calendar", methods=["GET"])
def calendar():
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
    return jsonify({"suggestion": "Remember to stay hydrated!"})

@app.route("/ai-assistant", methods=["POST"])
def ai_assistant():
    data = request.get_json()
    voice_input   = data.get("voice_input", "")
    calendar_data = data.get("calendar", {})
    weather_data  = data.get("weather", {})
    identity      = data.get("identity", "")

    prompt = (
        f"You are an AI assistant with the identity '{identity}'. "
        f"Here is the calendar data: {calendar_data}. "
        f"Here is the weather data: {weather_data}. "
        f"User said: {voice_input}. "
        "Please provide a helpful and concise response."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        response_text = response.choices[0].message.content.strip()
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"Error contacting OpenAI: {e}"}), 500

@app.route("/test", methods=["POST"])
def test_connection():
    data  = request.get_json()
    query = data.get("query", "")
    return jsonify({"response": f"Mornova here 👋 I received: '{query}'"})

# --- New Status Endpoint for Pi Integration ---

@app.route("/status", methods=["GET"])
def status():
    data = get_weather_forecast()
    # handle weather-api errors
    if "error" in data:
        return jsonify({"error": data["error"]}), 502

    # decide lamp color based on rain chance
    if data.get("daily_chance_of_rain", 0) > 90:
        weather_state = "rainy"   # Pi will map this to blue
    else:
        weather_state = "other"   # Pi will map this to warm white

    # generate AI message for the speaker
    ai_prompt = f"Write a friendly one-sentence update about today's weather: {data}"
    ai_resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": ai_prompt}],
        max_tokens=50
    )
    message = ai_resp.choices[0].message.content.strip()

    return jsonify({
        "weather": weather_state,
        "message": message
    })

if __name__ == "__main__":
    # listen on all IPs at port 5001 so your Pi can reach it
    app.run(host="0.0.0.0", port=5001, debug=True)
