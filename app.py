
import asyncio
import json
import os
import queue
import threading
import shutil
import tempfile
import concurrent.futures
from flask import Flask, render_template_string, request, send_file
from werkzeug.utils import secure_filename

from download import youtube_to_mp3
from collect_playlist import get_playlist_tracks
from collect_song_ids import search_video

app = Flask(__name__)

# In-memory queue to send progress updates to the frontend
progress_queue = queue.Queue()
completed_songs_counter = 0
completed_songs_lock = threading.Lock()

@app.route('/')
def index():
    return render_template_string(open('index.html').read())

@app.route('/download', methods=['POST'])
def download():
    playlist_id = request.form['playlist_id']
    output_dir_obj = tempfile.TemporaryDirectory()
    output_dir = output_dir_obj.name

    global completed_songs_counter
    completed_songs_counter = 0

    threading.Thread(target=download_playlist, args=(playlist_id, output_dir, progress_queue, output_dir_obj)).start()
    return "Downloading..."

@app.route('/progress')
def progress():
    def generate():
        while True:
            try:
                data = progress_queue.get(timeout=10)
                yield f"data: {json.dumps(data)}\n\n"
            except queue.Empty:
                # No new message in the queue
                pass
    return app.response_class(generate(), mimetype='text/event-stream')


def download_song(song, output_path, progress_queue, total_songs):
    global completed_songs_counter
    query = song["title"] + " " + song["artists"] + " lyrics"
    video_id = search_video(query)
    url = f"https://www.youtube.com/watch?v={video_id}"
    youtube_to_mp3(url, output_path)
    with completed_songs_lock:
        completed_songs_counter += 1
        progress_queue.put({'type': 'progress', 'current': completed_songs_counter, 'total': total_songs})

def download_playlist(playlist_id, output_path, progress_queue, output_dir_obj):
    playlist_id = extract_playlist_id(playlist_id)
    playlist = get_playlist_tracks(playlist_id)
    if not playlist:
        progress_queue.put({'type': 'error', 'message': 'Failed to retrieve playlist. Please check the playlist ID.'})
        return

    total_songs = len(playlist)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_song, song, output_path, progress_queue, total_songs) for song in playlist]
        concurrent.futures.wait(futures)

    zip_path = shutil.make_archive(output_path, 'zip', output_path)
    output_dir_obj.cleanup() # Clean up the temporary directory
    progress_queue.put({'type': 'complete', 'message': 'Playlist has been downloaded and converted to MP3!', 'zip_path': zip_path})

@app.route('/download_zip')
def download_zip():
    path = request.args.get('path')
    return send_file(path, as_attachment=True)

def extract_playlist_id(input_text):
    if "spotify.com/playlist/" in input_text:
        start = input_text.find("playlist/") + len("playlist/")
        end = input_text.find("?") if "?" in input_text else len(input_text)
        return input_text[start:end]
    return input_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
