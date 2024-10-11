import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from download import youtube_to_mp3
from collect_playlist import get_playlist_tracks
from collect_song_ids import search_video
import threading

# Function to download a playlist and convert each song to mp3
def download_playlist(playlist_id, output_path):
    playlist = get_playlist_tracks(playlist_id)
    if not playlist:
        messagebox.showerror("Error", "Failed to retrieve playlist. Please check the playlist ID.")
        return
    
    total_songs = len(playlist)
    progress_bar["maximum"] = total_songs  # Set the maximum value of the progress bar

    for idx, song in enumerate(playlist):
        query = song["title"] + " " + song["artists"] + " lyrics"
        video_id = search_video(query)
        url = f"https://www.youtube.com/watch?v={video_id}"
        youtube_to_mp3(url, output_path)
        progress_bar["value"] = idx + 1  # Update the progress bar value
        root.update_idletasks()  # Refresh the GUI to show progress

    messagebox.showinfo("Success", "Playlist has been downloaded and converted to MP3!")
    progress_bar["value"] = 0  # Reset progress bar after completion

# Browse for output directory
def browse_output_directory():
    folder_selected = filedialog.askdirectory()
    output_entry.delete(0, tk.END)  # Clear current text in the entry
    output_entry.insert(0, folder_selected)  # Insert the selected folder

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

    # Run the download process in a separate thread to avoid freezing the GUI
    threading.Thread(target=download_playlist, args=(playlist_id, output_path)).start()

# Set up the GUI
root = tk.Tk()
root.title("YouTube to MP3 Playlist Downloader")
root.geometry("500x300")  # Increase window size to accommodate progress bar

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

# Start the GUI event loop
root.mainloop()
