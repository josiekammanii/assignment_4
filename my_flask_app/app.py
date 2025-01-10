from flask import Flask, request, render_template, url_for, redirect
from my_classes import MusicManager, Artist, Album, AudioTrack
import os
import pandas as pd
import csv
from global_vars import CSV_SONGS_PATH,ALBUM_PATH,ARTIST_PATH

# Initialize Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'


# Create an instance of MusicManager
manager = MusicManager()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/view_songs')
def view_songs():
    return render_template('view_songs.html', songs=manager.songs)

@app.route('/view_songs/filter_genre', methods=['GET', 'POST'])
def filter_songs_by_genre():
    genre = request.args.get('genre') 
    songs = pd.read_csv(CSV_SONGS_PATH)
    if genre:
        songs = [song for song in manager.songs if song.genre.lower() == genre]
        print(songs)
    return render_template('view_songs.html', songs=songs)


def filter_songs_by_year(year):
    songs = pd.read_csv(CSV_SONGS_PATH)
    filtered_songs = songs[songs["Year"] == year]
    return filtered_songs

@app.route('/view_albums')
def view_albums():
    songs = pd.read_csv(CSV_SONGS_PATH)
    return render_template('view_albums.html',songs=manager.albums)

@app.route('/view_albums/<album_name>')
def view_album(album_name):
    albums = pd.read_csv(ALBUM_PATH)
    return render_template('album_page.html', "Dispalying album {album.album_name}", albums=albums, album_name=album_name)

@app.route('/view_artists')
def view_artists():
    songs = pd.read_csv(CSV_SONGS_PATH)
    return render_template('view_artists.html', songs=manager.artists)


@app.route('/view_playlists')
def view_playlists():
    return render_template('view_playlists.html', playlists=manager.playlists)

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    playlist_name = request.form.get('playlist_name')
    if playlist_name:
        if playlist_name not in manager.playlists:
            manager.playlists[playlist_name] = []  # Add a new playlist with an empty list for songs
            result = f"Playlist '{playlist_name}' created."
        else:
            result = f"Playlist '{playlist_name}' already exists!"
        return render_template('view_playlists.html', result=view_playlists, playlists=manager.playlists)
    else:
        return "Please provide a playlist name."
        

@app.route('/delete_playlist/<playlist_name>', methods=['POST'])
def delete_playlist(playlist_name):
    playlist_name = request.form.get('playlist_name')
    if playlist_name in manager.playlists:
        manager.playlists.remove[playlist_name]
        return render_template('view_playlists.html', result=view_playlists,playlists=manager.playlists)
    else:
        return f"Playlist {playlist_name} not found."



@app.route('/upload')
def upload():
    return render_template('upload_songs.html')

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['Name']
        artist_name = request.form['Artist']
        album_name = request.form['Album']
        duration = request.form['Duration']


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