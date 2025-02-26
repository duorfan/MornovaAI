import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Retrieve credentials
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

if not SPOTIPY_CLIENT_ID:
    raise ValueError("Missing SPOTIPY_CLIENT_ID. Check your .env file!")

print("Client ID Loaded:", SPOTIPY_CLIENT_ID[:5] + "*****")  # Debugging

# Define the required scope
SCOPE = "user-top-read"

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

def get_spotify_recommendations():
    """Fetches recommended songs based on the user's top tracks."""
    try:
        results = sp.current_user_top_tracks(limit=5, time_range='short_term')
        recommendations = [track["name"] for track in results["items"]]
        return {"recommendations": recommendations}
    except Exception as e:
        return {"error": str(e)}

# ✅ Add this for testing
if __name__ == "__main__":
    print(get_spotify_recommendations())
