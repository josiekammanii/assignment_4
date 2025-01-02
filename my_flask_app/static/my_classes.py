from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd
import csv

app = Flask(__name__)

# ----- Classes -----
class AudioTrack:
    def __init__(self, title, artist, duration,year_created,genre, album):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.year = year_created
        self.genre = genre
        self.album = album
        self.date_uploaded = datetime.now()

class Album():
    def __init__(self, name):
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

class MusicManager():
    def __init__(self):
        self.songs = []
        self.artists = []
        self.albums = []
        self.playlists = {}  # Dictionary to store playlists, where keys are playlist names

        self.load_songs_from_csv("popular_songs.csv") 
        print(self.songs)


    def load_songs_from_csv(self, file_path):
        # Read CSV file and populate self.songs
        data = pd.read_csv(file_path)  # Load CSV file
        for _, row in data.iterrows():
            artist = Artist(row["artist"])
            song = AudioTrack(row["song_title"], row["artist"], row["duration"], row["album"])
            album = Album(row["album"])
            self.songs.append(song)  # Add song as a dictionary to the list
            self.artists.append(artist)
            self.albums.append(album)

    def filter_songs_by_genre(self, genre):
        # Return all songs that match the given genre
        return [song for song in self.songs if song.genre == genre]
    def filter_songs_by_year_created(self, year):
        # Return all songs that were created on the given year
        return [song for song in self.songs if song.year_created == year]
       
    def create_playlist(self, playlist_name):
        if playlist_name in self.playlists:
            print(f"Playlist '{playlist_name}' Already Exists!")
        else:
            self.playlists[playlist_name] = []  # Initialize an empty list for the playlist
            print(f"Playlist '{playlist_name}' created.")


