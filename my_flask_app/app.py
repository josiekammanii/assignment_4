from flask import Flask, request, render_template
from models import MusicManager, Artist, Album, AudioTrack # Import the class from your models file
import os

# Initialize Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'


# Create an instance of MusicManager
manager = MusicManager()

# Load songs from "songs.csv"
manager.load_songs_from_csv("songs.csv")

# Print all loaded songs to verify
print(manager.songs)

# ----- Data Storage -----
music_collection = {
    "artists": [],
    "albums": [],
    "songs": []
}


@app.route('/')
def home():
    return render_template('index.html', collection=music_collection)

@app.route('/view_songs')
def view_songs():
    return render_template('view_songs.html', songs=music_collection["songs"])

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form['title']
        artist_name = request.form['artist']
        duration = request.form['duration']
        album_name = request.form['album']

        # Check if artist exists
        artist = next((a for a in music_collection["artists"] if a.name == artist_name), None)
        if not artist:
            artist = Artist(artist_name)
            music_collection["artists"].append(artist)

        # Check if album exists
        album = next((a for a in music_collection["albums"] if a.name == album_name), None)
        if not album:
            album = Album(album_name)
            music_collection["albums"].append(album)
            artist.add_album(album)

        # Create the song
        song = AudioTrack(title, artist_name, duration, album_name)
        music_collection["songs"].append(song)
        artist.add_song(song)
        album.add_song(song)

        return redirect(url_for('home'))

# ----- Run the App -----
if __name__ == '__main__':
    app.run(debug=True)