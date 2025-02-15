from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_events():
    """Fetches upcoming events from Google Calendar."""
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
    events_result = service.events().list(calendarId="primary", maxResults=5, singleEvents=True, orderBy="startTime").execute()
    events = events_result.get("items", [])

    return events

if __name__ == "__main__":
    events = get_calendar_events()
    for event in events:
        print(event["summary"], event["start"]["dateTime"])
