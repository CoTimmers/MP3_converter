# MP3 Converter Project
The goal of this repo is to download songs from a Spotify playlist using a web interface.

## Prerequisites
- Docker and Docker Compose (recommended)
- OR Python 3.9 or higher

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/CoTimmers/MP3_converter.git
cd MP3_converter
```

### 2. Create .env file
Create a `.env` file in the project root containing:
- Spotify client ID - [Get one here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- Spotify secret client key - [Get one here](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)
- YouTube API keys - [Get some here](https://developers.google.com/youtube/v3/getting-started?hl=fr)

Example `.env` file (keys are fictional):

```bash
SPOTIFY_CLIENT_ID = "9a71eedejece374hdncdjs248"
SPOTIFY_SECRET_CLIENT = "fc2c423hed3788h249"

YOUTUBE_API_KEYS = AIzaSyCZNWcJyeid348uejx,AIzaSyDCwsmPE68J0odeY6H
```

**DO NOT commit your .env file**

## Running the Application

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

Then open your browser to `http://localhost:5000`

To stop:
```bash
docker-compose down
```

### Option 2: Using Python directly

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

Then open your browser to `http://localhost:5000`

### Option 3: Using Poetry

```bash
# Install dependencies
poetry install

# Activate the virtual environment
poetry shell

# Run the Flask app
python app.py
```

Then open your browser to `http://localhost:5000`

## Usage

1. Open `http://localhost:5000` in your browser
2. Enter your Spotify playlist ID or URL
   - To find the playlist ID: Browse to your Spotify playlist → Click the three dots → Share → Copy link to playlist
   - You can paste either the full URL or just the playlist ID
3. Click download and wait for the process to complete
4. Download the ZIP file containing all MP3s







# TO DO
- Improve user interface
- Handle multiple downloads

