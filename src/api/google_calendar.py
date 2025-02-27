from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build
from datetime import datetime, timezone

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_next_event():
    """Fetches the next upcoming event from Google Calendar."""
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
        maxResults=10,  # Fetch more to ensure at least one valid event
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return "No upcoming events."

    # Return only the next event
    next_event = events[0]

    return {
        "summary": next_event.get("summary", "No Title"),
        "start": next_event["start"]["dateTime"],
        "end": next_event["end"]["dateTime"],
        "timeZone": next_event["start"].get("timeZone", "UTC"),
        "location": next_event.get("location", "No location"),
        "htmlLink": next_event.get("htmlLink", ""),
        "status": next_event.get("status", ""),
        "attendees": next_event.get("attendees", [])
    }

if __name__ == "__main__":
    next_event = get_next_event()
    print(next_event)
