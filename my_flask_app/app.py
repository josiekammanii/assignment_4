from flask import Flask, request, render_template, url_for, redirect
from my_classes import MusicManager, Artist, Album, AudioTrack
import os
import pandas as pd
import csv
from global_vars import CSV_SONGS_PATH,ALBUM_PATH,ARTIST_PATH
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Initialize Flask App
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

IMAGE_FOLDER = "static/images"
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)

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

@app.route('/view_playlists/<playlist_name>')
def view_playlist(playlist_name):
    albums = pd.read_csv(ALBUM_PATH)
    return render_template('album_page.html', albums=albums, album_name=album_name)

@app.route('/upload')
def upload():
    return render_template('upload_songs.html')

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form.get('title')
        playlist = request.form.get('playlist')

        if playlist in manager.playlists:
            song = next((song for song in manager.songs if song.title == title), None)
            if song:
                manager.playlists[playlist].append(song)
                print(f"Song '{song}' added to playlist '{playlist}'.")
                return render_template('view_songs.html', songs=manager.songs)
            else:
                print(f"Song '{song}' not found.")
    
@app.route('/collection_statistics')
def statistics():
    music_stats = pd.read_csv(CSV_SONGS_PATH)
    
    # Generate and save Pie Chart
    plt.figure(figsize=(8, 5.5))
    pie_chart = music_stats['Genre'].value_counts().plot.pie(autopct='%1.1f%%',pctdistance = 0.9,labeldistance = 1.05,radius=1.5)
    pie_chart_path = os.path.join(IMAGE_FOLDER, "pie_chart.png")
    plt.savefig(pie_chart_path)
    plt.close()
    
    # Generate and save Bar Chart
    plt.figure(figsize=(12, 14)) 
    bar_chart = music_stats['Artist'].value_counts().plot.bar()
    plt.title("Artist Distribution")
    plt.xticks(fontsize=7)
    bar_chart_path = os.path.join(IMAGE_FOLDER, "bar_chart.png")
    plt.savefig(bar_chart_path)
    plt.close()
    
    # Generate and save Line Chart
    line_chart = music_stats['Year'].value_counts().sort_index().plot.line()
    plt.title("Songs in a Year")
    line_chart_path = os.path.join(IMAGE_FOLDER, "line_chart.png")
    plt.savefig(line_chart_path)
    plt.close()
    
    # Pass image paths to the template
    return render_template('statistics.html', 
                           pie_chart_url=pie_chart_path, 
                           bar_chart_url=bar_chart_path, 
                           line_chart_url=line_chart_path)



# ----- Run the App -----
if __name__ == '__main__':
    app.run(debug=True)