import imageio_ffmpeg
from yt_dlp import YoutubeDL
import os

def youtube_to_mp3(url, output_path="output"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe(),  # Use imageio's ffmpeg location
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Downloaded and converted to MP3")


