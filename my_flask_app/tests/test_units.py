import unittest
from my_flask_app import app

class BasicTests(unittest.TestCase):

         # executed prior to each test
         def setUp(self):
              app.config['TESTING'] = True
              app.config['WTF_CSRF_ENABLED'] = False
              app.config['DEBUG'] = False
              self.app = app.test_client()

         # executed after each test
         def tearDown(self):
              pass

         # test if the home page loads correctly
         def test_home_page(self):
              response = self.app.get('/', follow_redirects=True)
              self.assertEqual(response.status_code, 200)
              self.assertIn(b'Welcome to the Home Page', response.data)

         # test if the about view songs loads correctly
         def test_about_page(self):
              response = self.app.get('/view_songs', follow_redirects=True)
              self.assertEqual(response.status_code, 200)
              self.assertIn(b'View Songs', response.data)

         # test if a non-existent page returns a 404 error
         def test_404_page(self):
              response = self.app.get('/non_existent_page', follow_redirects=True)
              self.assertEqual(response.status_code, 404)

         # test if the contact page loads correctly
         def test_contact_page(self):
              response = self.app.get('/contact', follow_redirects=True)
              self.assertEqual(response.status_code, 200)
              self.assertIn(b'Contact Us', response.data)

if __name__ == "__main__":
         unittest.main()
    

# 4. **Run your tests:**
#     You can run your tests using the following command:
#     ```sh
#     python -m unittest discover -s my_flask_app/tests
#     ```

#This setup will help you ensure that your Flask application is well-tested and follows best practices for unit testing.