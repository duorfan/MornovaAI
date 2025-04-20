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
    
@app.route("/test", methods=["POST"])
def test_connection():
    data = request.get_json()
    query = data.get("query", "")
    return jsonify({"response": f"Mornova here 👋 I received: '{query}'"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)


