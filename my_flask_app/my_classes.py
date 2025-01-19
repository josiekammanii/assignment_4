from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd
import csv
from global_vars import CSV_SONGS_PATH

app = Flask(__name__)

# ----- Classes -----

class AudioTrack():
    def __init__(self, title, artist,album, duration,year,genre):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.year = year
        self.genre = genre
        self.date_uploaded = datetime.now()

class MusicManager():
    def __init__(self):
        self.songs = []
        self.artists = []
        self.albums = []
        self.playlists = {}  # List to store playlists, where keys are playlist names

        self.load_songs_from_csv(CSV_SONGS_PATH) 


    def load_songs_from_csv(self, file_path):
        # Read CSV file and populate self.songs
        data = pd.read_csv(file_path)  # Load CSV file
        for _, row in data.iterrows():
            artist = Artist(row["Artist"])
            song = AudioTrack(row["Name"], row["Artist"],row["Album"], row["Duration"], row["Year"], row["Genre"])
            album = Album(row["Album"])
            self.songs.append(song)  # Add song as a dictionary to the list
            self.artists.append(artist)
            self.albums.append(album)


class Album():
    def __init__(self,name):
        self.name = name
        self.date_uploaded = datetime.now()
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

class Artist():
    def __init__(self, name):
        self.name = name
        self.albums = []
        self.songs = []

    def add_album(self, album):
        self.albums.append(album)

    def add_song(self, song):
        self.songs.append(song)

