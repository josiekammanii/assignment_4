from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# ----- Classes -----
class AudioTrack:
    def __init__(self, title, artist, duration, album=None):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.album = album
        self.date_uploaded = datetime.now()

class Album:
    def __init__(self, name):
        self.name = name
        self.date_uploaded = datetime.now()
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

class Artist:
    def __init__(self, name):
        self.name = name
        self.albums = []
        self.songs = []

    def add_album(self, album):
        self.albums.append(album)

    def add_song(self, song):
        self.songs.append(song)

class MusicManager:
    def __init__(self):
        self.songs = []

    def load_songs_from_csv(self, file_path):
        # Read CSV file and populate self.songs
        data = pd.read_csv(file_path)  # Load CSV file
        for _, row in data.iterrows():
            song = {
                "genre": row["genre"],
                "artist": row["artist"],
                "album": row["album"],
                "song_title": row["song_title"],
                "composer": row["composer"],
                "duration": row["duration"],
            }
            self.songs.append(song)  # Add song as a dictionary to the list


