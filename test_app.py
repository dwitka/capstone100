import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, db


assistant_token = os.environ.get('ASSISTANT_TOKEN')
director_token = os.environ.get('DIRECTOR_TOKEN')
executive_token = os.environ.get('EXECUTIVE_TOKEN')


class MainTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://postgres:postGres44@localhost:5432/hollywood'
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    One test for success behavior of each endpoint
    One test for error behavior of each endpoint
    """

    # Movie Tests
    def test_home_page(self):
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_post_movie_200(self):
        new_movie = {
            'title': 'Call Me by Your Name',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_missing_data_post_movie_422(self):
        new_movie = None
        auth = {
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().post('/movies', json=new_movie, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_movie_200(self):
        edit_movie = {
            'title': 'Yeahhh, patch works!!!',
            'release_date': '2020-11-01'
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().patch('/movies/3', json=edit_movie,
                                  headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_patch_movie_not_found_404(self):
        edit_movie = {
            'title': 'testing',
            'release_date': '2020-11-01'
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token) 
        }
        res = self.client().patch('/movies/90', json=edit_movie, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies_200(self):
        auth = {
            'Authorization': "Bearer {}".format(assistant_token)
        }
        res = self.client().get('/movies', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_not_auth_get_movies_401(self):
         res = self.client().get('/movies', headers='')
         data = json.loads(res.data)

         self.assertEqual(res.status_code, 401)
         self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_movie_200(self):
        auth = {
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().delete('/movies/2', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

    def test_delete_movie_not_found_404(self):
        auth = {
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().delete('/movies/55', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Actor Tests
    def test_post_actor_200(self):
        new_actor = {
            'name': 'Ronald Reagan',
            'age': 24,
            'gender': 'M',
            'movie_id': 6
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().post('/actors', json=new_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_missing_data_post_actor_422(self):
        new_actor = None
        auth = {
            'Authorization': "Bearer {}".format(executive_token)
        }
        res = self.client().post('/actors', json=new_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_patch_actor_200(self):
        edit_actor = {
            'name': 'Bob Dole', 
            'age': 92,
            'gender': 'M',
            'movie_id': ''
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().patch('/actors/3', json=edit_actor, headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_patch_actor_not_found_404(self):
        edit_actor = {
            'name': '',
            'age': 77,
            'gender': '',
            'movie_id': ''
        }
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().patch('/actors/1000', json=edit_actor,
                                  headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_actors_200(self):
        auth = {
            'Authorization': "Bearer {}".format(assistant_token)
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_unauth_get_actors_401(self):
        res = self.client().get('/actors', headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')

    def test_delete_actor_200(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().delete('/actors/4', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 4)

    def test_delete_actor_not_found_404(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
        }
        res = self.client().delete('/actors/55', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    # Authorization Tests
    def test_invalid_header_get_movies_401(self):
        auth = {
            'Authorization': "JWT {}".format(assistant_token)
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')

    def test_invalid_auth_get_actors_401(self):
        auth = {
            'Authorization': "Bearer{}".format(assistant_token)
        }
        res = self.client().get('/actors', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'invalid_header')

    def test_invalid_auth_add_actor_403(self):
        new_actor = {
            'name': 'Bob Dole',
            'age': 92,
            'gender': 'M',
            'movie_id': 5
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(assistant_token)
        }
        res = self.client().post('/actors', json=new_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'Sorry, you dont have permissions.')

    def test_invalid_auth_modify_movie_403(self):
        edit_movie = {
            'title': '',
            'release_date': '2020-11-11'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(assistant_token)
        }
        res = self.client().patch('/movies/4', json=edit_movie,
                                  headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'Sorry, you dont have permissions.')

    def test_invalid_auth_delete_movie_403(self):
        auth = {
            'Authorization': "Bearer {}".format(director_token)
            }
        res = self.client().delete('/movies/6', headers=auth)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'Sorry, you dont have permissions.')

    def test_invalid_auth_add_movie_403(self):
        new_movie = {
            'title': 'To test',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(director_token)
            }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['message'],
                         'Sorry, you dont have permissions.')
