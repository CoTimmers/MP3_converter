import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
import requests
import json
import base64

CLIENT_ID = config.SPOTIFY_CLIENT_ID
CLIENT_SECRET = config.SPOTIFY_SECRET_CLIENT

# Function to get the access token
def get_token():
   auth_string = CLIENT_ID + ":" + CLIENT_SECRET 
   auth_bytes = auth_string.encode("utf-8")
   auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")
   url= "https://accounts.spotify.com/api/token"
  
   headers = {
    "Authorization": "Basic " + auth_base64,
    "Content-Type": "application/x-www-form-urlencoded" 
   }
   data = {"grant_type": "client_credentials"}
   result = requests.post(url, headers=headers, data=data)
   json_result = json.loads(result.content)
   token = json_result["access_token"]
   return token

# Function to get authentication headers
def get_auth_token(token):
    return {"Authorization": "Bearer " + token}

# Function to get playlist tracks with titles and artists
def get_playlist_tracks(playlist_id):
    token = get_token()
    headers = get_auth_token(token)
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to get playlist: {response.status_code}")
        return

    playlist_data = response.json()
    tracks = playlist_data['items']

    # Extract titles and artists

    playlist = []

    for track_item in tracks:
        track = track_item['track']
        title = track['name']
        artists = " ".join([artist['name'] for artist in track['artists']])
        playlist.append({"title": title, "artists": artists })
    
    return playlist








