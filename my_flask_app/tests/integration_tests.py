import unittest
from app import app
from my_classes import MusicManager

class TestPlaylistIntegration(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_view_playlists(self):
        # Initially, playlists should be empty
        manager.playlists = {}  # Reset playlists for testing
        response = self.app.get('/view_playlists')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"No playlists available", response.data)  # Add this message to your HTML template for empty playlists

    def test_create_playlist(self):
        # Test creating a playlist
        manager.playlists = {}  # Reset playlists for testing
        response = self.app.post('/create_playlist', data={'playlist_name': 'My Playlist'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"My Playlist", response.data)  # Verify playlist name appears in the response
        self.assertIn("My Playlist", manager.playlists)  # Verify playlist added to manager.playlists

    def test_create_duplicate_playlist(self):
        # Test creating a duplicate playlist
        manager.playlists = {'My Playlist': []}  # Pre-populate with an existing playlist
        response = self.app.post('/create_playlist', data={'playlist_name': 'My Playlist'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Playlist 'My Playlist' already exists!", response.data)

    def test_delete_playlist(self):
        # Test deleting a playlist
        manager.playlists = {'My Playlist': []}  # Pre-populate with a playlist
        response = self.app.post('/delete_playlist/My Playlist', data={'playlist_name': 'My Playlist'})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("My Playlist", manager.playlists)  # Verify playlist removed from manager.playlists

    def test_delete_nonexistent_playlist(self):
        # Test deleting a playlist that doesn't exist
        manager.playlists = {}  
        response = self.app.post('/delete_playlist/Nonexistent', data={'playlist_name': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Playlist Nonexistent not found.", response.data)

if __name__ == '__main__':
    unittest.main()

