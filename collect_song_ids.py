import os
from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

# List of API keys
API_KEYS = os.getenv("YOUTUBE_API_KEYS").split(',')

# Keep track of the current API key index
current_key_index = 0

# Function to get a YouTube API client with the current API key
def get_youtube_client():
    return build('youtube', 'v3', developerKey=API_KEYS[current_key_index])

# Function to switch to the next API key
def switch_api_key():
    global current_key_index
    current_key_index += 1
    if current_key_index >= len(API_KEYS):
        raise Exception("All API keys have exceeded their quota.")
    print(f"Switching to API key {current_key_index + 1}")

# Example function using the YouTube API
def search_video(query):
    global youtube
    youtube = get_youtube_client()  # Get YouTube client with the current API key
    try:
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1,
        )
        response = request.execute()
        video_id = response['items'][0]['id']['videoId']
        return video_id
    

    except HttpError as e:
        if e.resp.status == 403 and 'quota' in str(e):
            print("Quota exceeded for the current API key.")
            switch_api_key()  # Switch to the next API key
            return search_video(query)  # Retry with the new key
        else:
            raise e  # Handle other errors normally







