import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

executive_token = os.environ['EXECUTIVE_TOKEN']

link = 'postgresql://postgres:postGres44@localhost:5432/trivia'

class EndPointsTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = link
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_root_200(self):
        res = self.client().get('/login')
        self.assertEqual(res.status_code, 200)

    def test_actors_200(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().get('/actors', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_200(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().get('/movies', headers=headers)
        self.assertEqual(res.status_code, 200)

    def test_post_movies_200(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_token)
        }
        new_movie = {
            'title': 'Matrix Reloaded',
            'release_date': '2003'
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie(self):
        auth = {
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().delete('/movies/21', headers=auth)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 21)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
