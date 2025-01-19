import unittest
import sys
import os
import pandas as pd
from flask import Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, manager
from my_classes import MusicManager, AudioTrack, Album, Artist  

class BasicTests(unittest.TestCase):

     # executed prior to each test
     def setUp(self):
          app.config['TESTING'] = True
          app.config['WTF_CSRF_ENABLED'] = False
          app.config['DEBUG'] = False
          self.app = app.test_client()
          self.app.testing = True

         # executed after each test
     def tearDown(self):
          pass

         # test if the home page loads correctly
     def test_home_page(self):
               response = self.app.get('/', follow_redirects=True)
               self.assertEqual(response.status_code, 200)
               self.assertIn(b"Welcome to your Music Collection Manager", response.data)

     # test if the about view songs loads correctly
     def test_about_page(self):
          response = self.app.get('/view_songs', follow_redirects=True)
          self.assertEqual(response.status_code, 200)
          self.assertIn(b'View Songs', response.data)
          self.assertIn(b'Filter By Genre', response.data)
          self.assertIn(b"Pop", response.data)  # Check if a mocked genre is in the response

     # test if a non-existent page returns a 404 error
     def test_404_page(self):
          response = self.app.get('/non_existent_page', follow_redirects=True)
          self.assertEqual(response.status_code, 404)
     
     
     class TestMusicManagerIntegration(unittest.TestCase): 
           
          def setUp(self):
               self.manager = MusicManager()
               self.manager.songs = []
               self.manager.artists = []
               self.manager.albums = []
               self.manager.playlists = {}

          def test_load_songs_from_csv(self):
               # Test loading songs from CSV file
               self.manager.load_songs_from_csv("tests/test_data/test_songs.csv")
               self.assertEqual(len(self.manager.songs), 3)
               self.assertEqual(len(self.manager.artists), 3)
               self.assertEqual(len(self.manager.albums), 3)
          
          def test_add_song(self):
               # Test adding a song
               new_song = AudioTrack("New Song", "New Artist", "New Album", "Pop", 2023)
               self.manager.add_song(new_song)
               self.assertEqual(len(self.manager.songs), 1)
               self.assertEqual(self.manager.songs[0].title, "New Song")

          def test_remove_song(self):
               # Test removing a song
               song_to_remove = AudioTrack("Song to Remove", "Artist", "Album", "Genre", 2022)
               self.manager.add_song(song_to_remove)
               self.manager.remove_song(song_to_remove)
               self.assertEqual(len(self.manager.songs), 0)

          def test_create_playlist(self):
               # Test creating a playlist
               self.manager.create_playlist("My Playlist")
               self.assertIn("My Playlist", self.manager.playlists)

          def test_add_song_to_playlist(self):
               # Test adding a song to a playlist
               song = AudioTrack("Playlist Song", "Artist", "Album", "Genre", 2022)
               self.manager.add_song(song)
               self.manager.create_playlist("My Playlist")
               self.manager.add_song_to_playlist("My Playlist", song)
               self.assertIn(song, self.manager.playlists["My Playlist"])

     
if __name__ == "__main__":
     unittest.main()