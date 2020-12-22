import os
import unittest
# from unittest.mock import patch
import json
from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy
from app import create_app
from models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth
# from flask_migrate import Migrate

import psycopg2


# database_filename = 'agancy_test.db'
# project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

Casting_Assistant = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBNeVJqZG5FNUJMei1KUzJYUFJoQSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b24tZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYzllNjM5MzFlMDIwMDZmMzZkYzIzIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODY1MTcyNiwiZXhwIjoxNjA4NjU4OTI2LCJhenAiOiJMdjZ5T296ZVVXSUtVbXZGY256ZHM2TzdjWm0xUFM0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.v56wQw0SxDc1_7k6OeItrpnj6XNakc1fLHoa_DJDpxYfXm_7UNbA1iPfqlZMzy2W6qujYipG9hdWQREJTQa9PdkeIyaNduOtP34G15jK7g75aaBi-2rrJzagEZhw7dR5BVvy3AWBIpK5JN_4k73VXctJH_mW96021h83HPFHUWvk2g45StP46TIFm0HlOkPpXogmO36EwQGIA42TaizzT5_mPJ4p6Q4HfC5gs94JHow3WeAT1qg6PIgEGXNjE2LgTLjdeeH7wTH-UwzP3wnOUE98lUiuNhjZ1AoqVHajY8VRJDzFliS0WJ6VuBcPMVAhNs9OgGxR60LmLNpFKGQC4g') 
Casting_Director = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBNeVJqZG5FNUJMei1KUzJYUFJoQSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b24tZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYzllZWM2ZTBmZmUwMDc1ZGI0MTBkIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODY1MTgyMSwiZXhwIjoxNjA4NjU5MDIxLCJhenAiOiJMdjZ5T296ZVVXSUtVbXZGY256ZHM2TzdjWm0xUFM0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.SikltrPHy5jpR7WMyVFwFP4l56RNqq7MhQRqzVlYugiIbavUkJ40uHWKi9zu2Fwe-I-PTZWV47TWtnbJdbzQ2y-wei1SMteNRKhfzerD5C66BNVYn-eg2WEGO182nQMYXnbWNwJpnKkxFQLAe8Mb_NzToySWUYsEC87aTCTD1IUL1uEiP-o5u_8cQpIByoxKUxl7YAOQ2z0rkqU3J5HzNUYEWsSNKuDYrg-2xx4MsaJVylzO5ox4cQ9Ia76HfK9N7C87O93ZxhHl06Vl170VTGIw4zOUJvtnjwrfc7PaPJZvkiYFmWcUqhKCxN5pPjpwlBeXZoFPBYUOD2iiBU2RFQ')  
Executive_Producer = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBNeVJqZG5FNUJMei1KUzJYUFJoQSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b24tZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZkYzlmNDI3NTY3OTcwMDY5MDg3YzBjIiwiYXVkIjoiY2Fwc3RvbiIsImlhdCI6MTYwODY1MTg4MSwiZXhwIjoxNjA4NjU5MDgxLCJhenAiOiJMdjZ5T296ZVVXSUtVbXZGY256ZHM2TzdjWm0xUFM0byIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.kyn3k_nspbCx4zyfX5pr4AAvyuPJfGc7oW0lIUiSdwnrGLXtQZw9mS5tWxbv850612hmI_sdoLGqjQbC1OLQDvpHmDHB22sOIj_aLx7XYygFRQtZS6sNNAb6oPxnRbWpPVWgvqFzcQZXhib3G9BYc_tNn4R89CY--DmEADmI-Usx5lWMtnutjbdzh0qqf1iYGgERpFaFX_dkWXF_dJafLOw9cOZKFCTw0FY7gLBoaFvGL_LfRfMOxUZ4ceH_Phmcz5713lQlK3gPchn4M-au-xX7xIv0fB3A7as0drIsYKXKcRP96h0-SpUDfiTq_C-oQOsXLvKU8qgXlLJ3AENRwg') 


class CapstonTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agancy_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # migrate = Migrate(self.app, db)

        self.new_movie = {
            'title': 'new movie 10',
            'release_date': '19-12-2020'
        }

        self.new_actors = {
            'name': 'new actor',
            'age': '22',
            'gender':'female'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    
    def tearDown(self):
        """Executed after reach test"""
        pass
    

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_movies(self):

        res = self.client().get('/movies', headers={"Authorization": "Bearer " + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['movies']))

    
    def test_401_authorization_header_missing(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,401)
        self.assertEqual(data['code'],'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected.')

    def test_create_new_movies(self):

        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    
    def test_422_if_movie_creation_fails(self):
        res = self.client().post('/movies', json={}, headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_401_Unauthorized(self):
        res = self.client().post('/movies', json=self.new_movie, headers = {"Authorization": "Bearer " + Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,401)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'Unauthorized')


    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        movies = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_update_movies(self):
        res = self.client().patch('/movies/3', json ={'title':'update','release_date':'10-10-2019'}, headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        movies = Movie.query.filter(Movie.id == 3).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['movies']))

    
    def test_404_update_movies_fails(self):
        res = self.client().patch('/movies/200', json ={'title':'update1','release_date':'10-10-2019'}, headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')


    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue((data['actors']))
    

    def test_create_new_actors(self):

        res = self.client().post('/actors', json=self.new_actors, headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        # question = Question.query.filter(Question.id == new_question.id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        
        # self.assertEqual(question)

    
    def test_422_if_actors_creation_fails(self):
        res = self.client().post('/actors', json={}, headers={"Authorization": "Bearer " + Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)
        

    def test_404_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


    def test_update_actors(self):
        res = self.client().patch('/actors/2', json=self.new_actors, headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['actors']))

    
    def test_404_update_actors_fails(self):
        res = self.client().patch('/actors/200', json=self.new_actors, headers={"Authorization": "Bearer " + Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')


if __name__ == '__main__':
    unittest.main()