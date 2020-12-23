import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth


Casting_Assistant = os.environ['Casting_Assistant']
Casting_Director = os.environ['Casting_Director']
Executive_Producer = os.environ['Executive_Producer']


class CapstonTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agancy_test"
        self.database_path = "postgres://{}/{}".format(
                                                        'localhost:5432',
                                                        self.database_name
                                                        )
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'new movie 20',
            'release_date': '19-12-2020'
        }

        self.new_actors = {
            'name': 'new actor',
            'age': '22',
            'gender': 'female'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):

        res = self.client().get(
                                '/movies',
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Assistant)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_401_authorization_header_missing(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(
                        data['description'],
                        'Authorization header is expected.'
                        )

    def test_create_new_movies(self):

        res = self.client().post(
                                '/movies',
                                json=self.new_movie,
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Executive_Producer)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_422_if_movie_creation_fails(self):
        res = self.client().post(
                                '/movies',
                                json={},
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Executive_Producer)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_401_Unauthorized(self):
        res = self.client().post(
                                '/movies',
                                json=self.new_movie,
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Assistant)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_delete_movie(self):
        res = self.client().delete(
                                    '/movies/4',
                                    headers={
                                        "Authorization":
                                        "Bearer " + str(Executive_Producer)
                                        }
                                    )
        data = json.loads(res.data)

        movies = Movie.query.filter(Movie.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete(
                                    '/movies/1000',
                                    headers={
                                        "Authorization":
                                        "Bearer " + str(Executive_Producer)
                                        }
                                    )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_movies(self):
        res = self.client().patch(
                                '/movies/3',
                                json={
                                    'title': 'update',
                                    'release_date': '10-10-2019'
                                    },
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Director)
                                    }
                                )
        data = json.loads(res.data)

        movies = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_update_movies_fails(self):
        res = self.client().patch(
                                '/movies/200',
                                json={
                                    'title': 'update1',
                                    'release_date': '10-10-2019'
                                    },
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Director)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors(self):
        res = self.client().get(
                                '/actors',
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Director)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue((data['actors']))

    def test_create_new_actors(self):

        res = self.client().post(
                                '/actors',
                                json=self.new_actors,
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Executive_Producer)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_422_if_actors_creation_fails(self):
        res = self.client().post(
                                '/actors',
                                json={},
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Executive_Producer)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actors(self):
        res = self.client().delete(
                                    '/actors/3',
                                    headers={
                                        "Authorization":
                                        "Bearer " + str(Casting_Director)
                                        }
                                    )
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 3)

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete(
                                  '/actors/1000',
                                  headers={
                                      "Authorization":
                                      "Bearer " + str(Casting_Director)
                                      }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_actors(self):
        res = self.client().patch(
                                '/actors/4', json=self.new_actors,
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Director)
                                    }
                                )
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_update_actors_fails(self):
        res = self.client().patch(
                                '/actors/200', json=self.new_actors,
                                headers={
                                    "Authorization":
                                    "Bearer " + str(Casting_Director)
                                    }
                                )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == '__main__':
    unittest.main()
