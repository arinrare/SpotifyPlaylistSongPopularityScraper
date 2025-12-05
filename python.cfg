# Load environment variables from .env file
from dotenv import load_dotenv
import os
load_dotenv()
# config.py
# Place your configuration variables here

# Spotify API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Playlist name (for reference, not used in scraping)
PUBLIC_PLAYLIST_URL = "https://open.spotify.com/playlist/5EG3CtFHeR228uLcOxMkTG"

# Weights for merged ranking (out of 100)
WEIGHT_PLAYLIST = 70  # Playlist popularity weight
WEIGHT_SPOTIFY = 30  # Spotify popularity weight
