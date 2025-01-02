from flask import Flask, request, render_template, url_for, redirect
from my_classes import MusicManager, Artist, Album, AudioTrack
import os
import pandas as pd
import csv

# Initialize Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'


# Create an instance of MusicManager
manager = MusicManager()


# Print all loaded songs to verify
print(manager.songs)

# ----- Data Storage -----
# music_collection = {
#     "artists": [],
#     "albums": [],
#     "songs": []
# }


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view_songs')
def view_songs():
    songs = pd.read_csv("popular_songs.csv", "r")
    return render_template('view_songs.html', songs=manager.songs)

@app.route('/view_albums')
def view_albums():
    songs = pd.read_csv("popular_songs.csv","r")
    albums = list({song["album"] for song in songs})
    return render_template('view_albums.html', songs=manager.albums)

@app.route('/view_artists')
def view_artists():
    songs = pd.read_csv("popular_songs.csv","r")
    # Extract unique artists
    artists = list({song["artist"] for song in songs})
    return render_template('view_artists.html', artists=manager.artists)


@app.route('/upload')
def upload():
    return render_template('upload_songs.html')

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist_name = request.form['artist']
        duration = request.form['duration']
        album_name = request.form['album']

        # Check if artist exists
        _artist = next((artist for artist in manager.artists if artist.name == artist_name), None)
        if not _artist:
            new_artist = Artist(artist_name)
            manager.artists.append(new_artist)

        # Check if album exists
        _album = next((album for album in manager.album if album.name == album_name), None)
        if not _album:
            new_album = Album(album_name)
            manager.albums.append(new_album)
            manager.artists.append(new_album)

        # Create the song
        song = AudioTrack(title, artist_name, duration, album_name)
        manager.songs.append(song)
        this_artist = next((artist for artist in manager.artists if artist.name == artist_name))
        this_artist.add_song(song)
        this_album = next((album for album in manager.albums if album.name == album_name))
        this_album.add_song(song)

        return redirect(url_for('home'))














# ----- Run the App -----
if __name__ == '__main__':
    app.run(debug=True)