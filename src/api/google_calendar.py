from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_next_events():
    """Fetches the next upcoming events from Google Calendar (up to 3 events)."""
    creds = None

    # Check if token exists (to avoid login every time)
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # Connect to Calendar API
    service = build("calendar", "v3", credentials=creds)
    
    # Get current time in UTC format
    now = datetime.now(timezone.utc).isoformat()

    # Fetch upcoming events
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,  # Fetch only future events
        maxResults=10,  # Fetch more to ensure we get at least 3 events
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return []

    next_events = []
    for event in events[:3]:
        next_events.append({
            "summary": event.get("summary", "No Title"),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
            "timeZone": event["start"].get("timeZone", "UTC"),
            "location": event.get("location", "No location"),
            "htmlLink": event.get("htmlLink", ""),
            "status": event.get("status", ""),
            "attendees": event.get("attendees", [])
        })
    return next_events

if __name__ == "__main__":
    events = get_next_events()
    print(events)
