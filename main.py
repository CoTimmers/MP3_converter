import tkinter as tk
import threading
import queue
from tkinter import filedialog, messagebox, ttk
from download import youtube_to_mp3
from collect_playlist import get_playlist_tracks
from collect_song_ids import search_video


# Function to download a playlist and convert each song to mp3
def download_playlist(playlist_id, output_path, progress_queue):
    playlist_id = extract_playlist_id(playlist_id)
    playlist = get_playlist_tracks(playlist_id)
    if not playlist:
        progress_queue.put(("error", "Failed to retrieve playlist. Please check the playlist ID."))
        return
    
    total_songs = len(playlist)
    for idx, song in enumerate(playlist):
        query = song["title"] + " " + song["artists"] + " lyrics"
        video_id = search_video(query)
        url = f"https://www.youtube.com/watch?v={video_id}"
        youtube_to_mp3(url, output_path)
        progress_queue.put(("progress", idx + 1, total_songs))  # Send progress to the queue

    progress_queue.put(("complete", "Playlist has been downloaded and converted to MP3!"))

# Extract playlist ID from URL or validate ID
def extract_playlist_id(input_text):
    if "spotify.com/playlist/" in input_text:
        # Extract ID from URL
        start = input_text.find("playlist/") + len("playlist/")
        end = input_text.find("?") if "?" in input_text else len(input_text)
        return input_text[start:end]
    return input_text

# Function to handle progress updates from the queue
def handle_progress():
    try:
        while not progress_queue.empty():
            msg = progress_queue.get_nowait()
            if msg[0] == "progress":
                _, current, total = msg
                progress_bar["value"] = current
                progress_bar["maximum"] = total
            elif msg[0] == "error":
                messagebox.showerror("Error", msg[1])
                return
            elif msg[0] == "complete":
                messagebox.showinfo("Success", msg[1])
                progress_bar["value"] = 0  # Reset progress bar after completion
    except queue.Empty:
        pass
    finally:
        # Check the queue again after 100ms
        root.after(100, handle_progress)

# Browse for output directory
def browse_output_directory():
    folder_selected = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_selected)

# Start the download process
def start_download():
    playlist_id = playlist_entry.get()
    output_path = output_entry.get()

    if not playlist_id:
        messagebox.showwarning("Input Error", "Please enter a Spotify playlist ID.")
        return

    if not output_path:
        messagebox.showwarning("Input Error", "Please select an output folder.")
        return

    # Run the download process in a separate thread
    threading.Thread(target=download_playlist, args=(playlist_id, output_path, progress_queue), daemon=True).start()

# Set up the GUI
root = tk.Tk()
root.title("YouTube to MP3 Playlist Downloader")
root.geometry("500x300")

progress_queue = queue.Queue()

# Label and entry for Spotify Playlist ID
tk.Label(root, text="Spotify Playlist ID:").grid(row=0, column=0, padx=10, pady=10)
playlist_entry = tk.Entry(root, width=50)
playlist_entry.grid(row=0, column=1, padx=10, pady=10)

# Label and entry for Output Directory
tk.Label(root, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Browse", command=browse_output_directory)
browse_button.grid(row=1, column=2, padx=10, pady=10)

# Download button
download_button = tk.Button(root, text="Download Playlist", command=start_download)
download_button.grid(row=2, column=1, pady=20)

# Progress bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start handling progress updates
root.after(100, handle_progress)

# Start the GUI event loop
root.mainloop()
