# main.py
from src.api.weather_api import get_weather_data
from src.api.google_calendar import get_calendar_events
from src.api.spotify import get_sleep_music
from src.ai.assistant import generate_wake_up_suggestion

def main():
    print("🌞 Mornova AI - Wake-up Time Adjuster 🌞")

    weather = get_weather_data()
    calendar = get_calendar_events()
    music = get_sleep_music()

    wake_up_time = generate_wake_up_suggestion(weather, calendar, music)

    print(f"📅 Recommended wake-up time: {wake_up_time}")

if __name__ == "__main__":
    main()
