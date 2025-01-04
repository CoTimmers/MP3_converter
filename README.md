# MP3 Converter Project
The goal of this repo is to download songs from a Spotify playlist

## Requirements
- Python 3.9 or higher
- Poetry for dependency management, you can find here how to install it: https://python-poetry.org/docs/

## Installation through poetry

### Cloning git repo
```bash
git clone https://github.com/CoTimmers/MP3_converter.git
```
Navigate to the MP3 COnverter folder inside your terminal. Install dependencies using Poetry:
```bash
poetry install
```
This will create a virtual environment (.venv), please ensure it has been created inside the root of this repo.
To run files inside your environment you need to activate it by running the following command : 
```bash
poetry shell
```
### Add necessary files/folders
Please add .env file at the root of this repo containing: 
- Spotify client ID, find here how to get one https://developer.spotify.com/documentation/web-api/tutorials/getting-started
- Spotify secret client key, find here how to get one https://developer.spotify.com/documentation/web-api/tutorials/getting-started
- Youtube API keys, find here how to get some https://developers.google.com/youtube/v3/getting-started?hl=fr
  
The .env file should be as in the following example (the keys are fictionnal)

```bash
SPOTIFY_CLIENT_ID = "9a71eedejece374hdncdjs248"
SPOTIFY_SECRET_CLIENT = "fc2c423hed3788h249"

YOUTUBE_API_KEYS = AIzaSyCZNWcJyeid348uejx,AIzaSyDCwsmPE68J0odeY6H
```
DO NOT commit your .env file  
## Running

Run the main.py file. 
Then enter the playlist ID. To find the playlist ID please browse to your spotify playlist, click on the three dots next to the playlist -> share -> copy link to the playlist. Paste that in the Spotify playlist ID field.







# TO DO
- Improve user interface
- Handle multiple downloads

