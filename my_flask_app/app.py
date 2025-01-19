from flask import Flask, request, render_template, url_for, redirect, jsonify
from my_classes import MusicManager, Artist, Album, AudioTrack
import os
import pandas as pd
import csv
from global_vars import CSV_SONGS_PATH,ARTIST_PATH
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.express as px



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

@app.route('/view_artists')
def view_artists():
    songs = pd.read_csv(ARTIST_PATH)
    return render_template('view_artists.html', songs=manager.artists)

SPOTIFY_LINKS = { "The Weeknd" : "https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ?si=7jkhSwoDQie6rL2OuOMJLQ", 
                 "Harry Styles" : "https://open.spotify.com/artist/6KImCVD70vtIoJWnq6nGn3?si=2Z2N1v3zQ8iQ1cYzJrJw5Q",
                 "Radiohead": "https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb?si=8Y6Q2I2oR9qZ1ZzT1tQ4Yw",
                 "Queen": "https://open.spotify.com/artist/1dfeR4HaWDbWqFHLkxsg1d?si=3lLZx8HhRv6g5Ld3j4fJ3w",
                 "Ed Sheeran": "https://open.spotify.com/artist/6eUKZXaKkcviH0Ku9w2n3V?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Bob Marley & The Wailers": "https://open.spotify.com/artist/2QsynagSdAqZj3U9HgDzjD?si=P3SyNkjWRLm3BCzTaPWIZg",
                 "Drake": "https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Whitney Houston": "https://open.spotify.com/artist/6XpaIBNiVzIetEPCWDvAFP?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Houston, Whitney": "https://open.spotify.com/artist/6XpaIBNiVzIetEPCWDvAFP?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Michael Jackson": "https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Destiny's Child": "https://open.spotify.com/artist/1Y8cdNmUJH7yBTd9yOvr5i?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Santana": "https://open.spotify.com/artist/6GI52t8N5F02MxU0g5U69P?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Savage Garden": "https://open.spotify.com/artist/3NRFinRTEqUCfaTTZmk8ek?si=6EknTSk4TCWxWY0RJtcf_Q",
                 "Madonna": "https://open.spotify.com/artist/6tbjWDEIzxoDsBA1FuhfPW?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Aguilera, Christina": "https://open.spotify.com/artist/1l7ZsJRRS8wlW3WfJfPfNS?si=lqLUbqvsRaSRpa56nSqKaA",
                 "Janet Jackson": "https://open.spotify.com/artist/3jOstUTkEu2JkjvRdBA5Gu?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Iglesias, Enrique": "https://open.spotify.com/artist/7qG3b048QCHVRO5Pv1T5lw?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Sisqo": "https://open.spotify.com/artist/6x9QLdzo6eBZxJ1bHsDkjg?si=NdmUID8QSgqZMkK8vl_9Bw",
                 "Lonestar": "https://open.spotify.com/artist/1Y8cdNmUJH7yBTd9yOvr5i?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "N'Sync": "https://open.spotify.com/artist/6GSxZb3opQJ4ZCjv4wJ1A8?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Vertical Horizon": "https://open.spotify.com/artist/6Hizgjo92FnMp8wGaRUNTn?si=YamYhQ5CShyVK11Hmc2WzQ",
                 "Creed": "https://open.spotify.com/artist/43sZBwHjahUvgbx1WNIkIz?si=rqErm_EaSrikk7ys8GmJxg",
                 "Aaliyah": "https://open.spotify.com/artist/0urTpYCsixqZwgNTkPJOJ4?si=gf3mBr3KRJSy33oA9pboVQ",
                 "matchbox twenty": "https://open.spotify.com/artist/3Ngh2zDBRPEriyxQDAMKd1?si=_ZqrDjNQQvqXlDThfT_bEw",
                 "Carey, Mariah": "https://open.spotify.com/artist/4iHNK0tOyZPYnBU7nGAgpQ?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Hill, Faith": "https://open.spotify.com/artist/25NQNriVT2YbSW80ILRWJa?si=DL9sl4bDT9u4Eq25-oKfJw",
                 "Mya": "https://open.spotify.com/artist/5tth2a3v0sWwV1C7bApBdX?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Dream": "https://open.spotify.com/artist/7qG3b048QCHVRO5Pv1T5lw?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Braxton, Toni": "https://open.spotify.com/artist/3X458ddYA2YcVWuVIGGOYe?si=A7NTo8tGTHmYr9Ep_eMKeg",
                 "Anthony, Marc": "https://open.spotify.com/artist/3TVXtAsR1Inumwj472S9r4?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "98 Degrees": "https://open.spotify.com/artist/6V03b3Y36lolYP2orXn8mV?si=2lsxJUx0Tpap8-1gWsumCg",
                 "3 Doors Down": "https://open.spotify.com/artist/2RTUTCvo6onsAnheUk3aL9?si=C8eScq4EQ3mTbvc3VY3T7A",
                 "Joe": "https://open.spotify.com/artist/3zTOe1BtyTkwNvYZOxXktX?si=uFEcJb1UTO-4N107HBOmMg",
                 "Jordan Montell": "https://open.spotify.com/artist/0iVrCROxeyon7MZUW3MfzT?si=2CtnJ4d5SqepMOsf-XHMGw",
                 "Emimen": "https://open.spotify.com/artist/7dGJo4pcD2V6oG8kP0tJRR?si=MvbaSAL3SEKQAB0t4nYY1Q",
                 "Pink": "https://open.spotify.com/artist/1KCSPY1glIKqW2TotWuXOR?si=qVqDvGnXTG6847p2FFBDHA",
                 "Samantha Mumba": "https://open.spotify.com/artist/1nSRa2YjjFWJLHGKM07oGQ?si=pyn0f8gUQyCQ2Hg5A8PrWA",
                 "Blaque": "https://open.spotify.com/artist/1nSRa2YjjFWJLHGKM07oGQ?si=m3sA4L9WQjazonOFzRJmwQ",
                 "Elliot, Missy Misdemeanor": "https://open.spotify.com/artist/2wIVse2owClT7go1WT98tk?si=fgYI0bVkSRa72kzhkzOZgg",
                 "Gray,Macy": "https://open.spotify.com/artist/4ylR3zwA0zaapAu94fktwa?si=YeXlI2xRT4CZ0cyMWnZ5aA",
                 "Ruff Endz": "https://open.spotify.com/artist/7liFhc0PDIx8etigqd2WhW?si=APhie9W3T3-doHJB8zh8Cw",
                 "Usher": "https://open.spotify.com/artist/23zg3TcAtWQy7J6upgbUnj?si=nPYBpycqSveNgg0VYvm8hw",
                 "Bob Marley": "https://open.spotify.com/artist/2QsynagSdAqZj3U9HgDzjD?si=P3SyNkjWRLm3BCzTaPWIZg",
                 "Beyoncé": "https://open.spotify.com/artist/6vWDO969PvNqNYHIOW5v0m?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Burna Boy": "https://open.spotify.com/artist/3wcj11K77LjEY1PkEazffa?si=JSCCbndASia4bGCobz2p4Q",
                 "Nirvana": "https://open.spotify.com/artist/6olE6TJLqED3rqDCT0FyPh?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "TLC": "https://open.spotify.com/artist/0TImkz4nPqjegtVSMZnMRq?si=DpDWkRpnRZCS37BwL7zC-w",
                 "Guns N' Roses": "https://open.spotify.com/artist/3qm84nBOXUEQ2vnTfUTTFC?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Nelly": "https://open.spotify.com/artist/3q7HBObVc0L8jNeTe5Gofh?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Fela Kuti": "https://open.spotify.com/artist/6vWDO969PvNqNYHIOW5v0m?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Eagles": "https://open.spotify.com/artist/0ECwFtbIWEVNwjlrfc6xoL?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Mark Ronson ft Bruno Mars" : "https://open.spotify.com/artist/0du5cEVh5yTK9QJze8zA0C?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Sting" : "https://open.spotify.com/artist/0Ty63ceoRnnJKVEYP0VQpk?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "2Baba" : "https://open.spotify.com/artist/2n4DcAtRMvfyRX3ljeC8Kp?si=M22rqwBARESOOVNCv3iAmw",
                 "Adele" : "https://open.spotify.com/artist/4dpARuHxo51G3z768sgnrY?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Shakira ft.Wyclef Jean" : "https://open.spotify.com/artist/0EmeFodog0BfCgMzAIvKQp?si=JqV3EA0uSKSfZdm0_lbBaw",
                 "Kendrick Lamar" : "https://open.spotify.com/artist/2YZyLoL8N0Wb9xBt1NhZWg?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Lauryn Hill" : "https://open.spotify.com/artist/2Mu5NfyYm8n5iTomuKAEHl?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Dave Brubeck" : "https://open.spotify.com/artist/6MuOaGK4xj2YfPIzJdRjWt?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Luis Fonsi ft. Daddy Yankee" : "https://open.spotify.com/artist/4V8Sr092TqfHkfAA5fXXqG?si=5Q8sNl8mQ5m3L3V1JYkz5w",
                 "Shakira" : "https://open.spotify.com/artist/0EmeFodog0BfCgMzAIvKQp?si=JqV3EA0uSKSfZdm0_lbBaw",}



@app.route('/view_artists/<artist_name>')
def view_artist(artist_name):
    artist_name = artist_name.replace("_", " ")
    spotify_link = SPOTIFY_LINKS.get(artist_name)
    if spotify_link:
        return redirect(spotify_link)
    else:
        return f"Artist {artist_name} not found."


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
        del manager.playlists[playlist_name]
        return render_template('view_playlists.html', result=view_playlists,playlists=manager.playlists)
    else:
        return f"Playlist {playlist_name} not found."

@app.route('/view_playlists/<playlist_name>')
def view_playlist(playlist_name):
    songs = manager.playlists.get(playlist_name, [])
    return render_template('songs_in_playlist.html', playlist_name=playlist_name, songs=manager.playlists[playlist_name])

@app.route('/upload')
def upload():
    return render_template('upload_songs.html')

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        title = request.form.get('title')
        playlist = request.form.get('manager.playlist')

    if playlist and title:
        if playlist in manager.playlists:
            manager.playlists[playlist].append(title)
        else:
                manager.playlists[playlist] = [title]
                return jsonify({"success": True, "message": f"Song '{title}' added to playlist '{playlist}'."})
    return jsonify({"success": False, "message": "Please provide a playlist name and song title."})
            
    
@app.route('/collection_statistics')
def statistics():
    music_stats = pd.read_csv(CSV_SONGS_PATH)
    
    # Generate and save Pie Chart
    plt.figure(figsize=(8, 5.5))
    pie_chart = music_stats['Genre'].value_counts().plot.pie(autopct='%1.1f%%',pctdistance = 0.9,labeldistance = 1.05,radius=1.5)
    pie_chart_path = os.path.join(IMAGE_FOLDER, "pie_chart.svg")
    plt.savefig(pie_chart_path)
    plt.close()
    
    # Generate and save Bar Chart
    plt.figure(figsize=(8, 13))
    genre_stats = music_stats['Artist'].value_counts()
    bar_chart = genre_stats.plot.bar()
    bar_chart.set_xticklabels(bar_chart.get_xticklabels(), fontsize=7)
    bar_chart_path = os.path.join(IMAGE_FOLDER, "bar_chart.svg")
    plt.savefig(bar_chart_path)
    plt.close()
    
    # Generate and save Line Chart
    line_chart = music_stats['Year'].value_counts().sort_index().plot.line()
    plt.title("Songs in a Year")
    line_chart_path = os.path.join(IMAGE_FOLDER, "line_chart.svg")
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


