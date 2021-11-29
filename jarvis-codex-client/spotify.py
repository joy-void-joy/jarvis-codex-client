import spotipy
from spotipy.oauth2 import SpotifyOAuth as OAuth

spotify = spotipy.Spotify(auth_manager=OAuth(scope="user-read-recently-played,user-read-playback-state,user-top-read,app-remote-control,streaming,user-library-modify,user-library-read"))