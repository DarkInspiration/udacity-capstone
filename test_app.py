
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie
from auth.test_env import casting_assistant, casting_director, executive_producer


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            "Authorization": f"Bearer {casting_assistant}"}
        self.casting_director_header = {
            "Authorization": f"Bearer {casting_director}"}
        self.executive_producer_header = {
            "Authorization": f"Bearer {executive_producer}"}

        self.new_movie = {
            "title": "Test title",
            "release_date": "2020.04.19"
        }

        self.new_actor = {
            "name": "Test name",
            "gender": "Test gender",
            "age": 20
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            ''' Delete old data/reset DB '''
            self.old_actors = Actor.query.all()
            self.old_movies = Movie.query.all()
            if self.old_actors:
                for i in self.old_actors:
                    Actor.query.get(i.id).delete()

            if self.old_movies:
                for i in self.old_movies:
                    Movie.query.get(i.id).delete()

            ''' Insert test data '''
            Movie(title="Pre-set title", release_date="2020.04.20").insert()
            Actor(name="Pre-set name",
                  gender="Pre-set gender",
                  age=20).insert()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test
    for successful operation and for expected errors.
    """

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))

    def test_create_actor(self):
        res = self.client().get('/actors', headers=self.casting_director_header)
        data = json.loads(res.data)
        old_number_of_actors = data['total_actors']

        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_actors'], old_number_of_actors + 1)

    def test_delete_actor(self):
        res = self.client().get('/actors', headers=self.casting_director_header)
        data = json.loads(res.data)
        old_number_of_actors = data['total_actors']
        id_to_delete = data['actors'][-1]['id']

        res = self.client().delete(
            f'/actors/{id_to_delete}',
            headers=self.casting_director_header)
        data = json.loads(res.data)
        actor = Actor.query.filter(
            Actor.id == id_to_delete).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id_to_delete)
        self.assertEqual(data['total_actors'], old_number_of_actors - 1)
        self.assertEqual(actor, None)

    def test_patch_actor(self):
        res = self.client().get('/actors', headers=self.casting_director_header)
        data = json.loads(res.data)
        id_to_patch = data['actors'][-1]['id']

        res = self.client().patch(
            f'/actors/{id_to_patch}',
            json={
                "name": "Patched name",
                "age": 99,
                "gender": "female"},
            headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['updated'], {
                'age': 99, 'gender': 'female', 'id': id_to_patch, 'name': 'Patched name'})

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))

    def test_create_movie(self):
        res = self.client().get('/movies', headers=self.executive_producer_header)
        data = json.loads(res.data)
        old_number_of_movies = data['total_movies']

        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], old_number_of_movies + 1)

    def test_delete_movie(self):
        res = self.client().get('/movies', headers=self.executive_producer_header)
        data = json.loads(res.data)
        old_number_of_movies = data['total_movies']
        id_to_delete = data['movies'][-1]['id']

        res = self.client().delete(
            f'/movies/{id_to_delete}',
            headers=self.executive_producer_header)
        data = json.loads(res.data)
        movie = Movie.query.filter(
            Movie.id == id_to_delete).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], id_to_delete)
        self.assertEqual(data['total_movies'], old_number_of_movies - 1)
        self.assertEqual(movie, None)

    def test_patch_movie(self):
        res = self.client().get('/movies', headers=self.casting_director_header)
        data = json.loads(res.data)
        id_to_patch = data['movies'][-1]['id']

        res = self.client().patch(
            f'/movies/{id_to_patch}',
            json={
                "title": "Patched title",
                "release_date": "2099.01.01"},
            headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'],
                         {'release_date': 'Thu, 01 Jan 2099 00:00:00 GMT',
                          'title': 'Patched title',
                          'id': id_to_patch})

    def test_post_movies_400_bad_request(self):
        res = self.client().post('/movies', json={}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Bad request")

    def test_post_movies_401_unauthorized(self):
        res = self.client().post('/movies', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unauthorized")

    def test_post_movies_403_forbidden(self):
        res = self.client().post('/movies', json={}, headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Forbidden")

    def test_get_moviesa_404_not_found(self):
        res = self.client().get('/moviesa', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found")

    def test_delete_movies_405_not_allowed(self):
        res = self.client().delete('/movies', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Method not allowed")

    def test_patch_actors_422_unprocessable_entity(self):
        res = self.client().patch('/actors/9999', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Unprocessable entity")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
