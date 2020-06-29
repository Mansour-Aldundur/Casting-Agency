import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT = os.environ['CASTING_ASSISTANT']
CASTING_DIRECTOR = os.environ['CASTING_DIRECTOR']
EXECUTIVE_PRODUCER = os.environ['EXECUTIVE_PRODUCER']


unittest.TestLoader.sortTestMethodsUsing = None


class MovieCastTestCase(unittest.TestCase):
    '''
    This class represent the test case for the Casting Agency API
    '''

    def setUp(self):
        '''
        Define test variables and initialize app.
        '''

        self.app = create_app()
        self.client = self.app.test_client

        self.new_actor = {
            'name': 'Steve Carell',
            'age': 54,
            'gender': 'male'
        }
        self.invalid_actor = {
            'name': 'Faris Saleh',
            'gender': 'male'
        }
        self.new_movie = {
            'title': 'Hacksaw Ridge',
            'release_date': '10-10-2016',
        }
        self.invalid_movie = {
            'title': 'Najran brave heart 2',
        }

        setup_db(self.app)

    def tearDown(self):
        '''
        Executed after reach test
        '''
        pass

    '''
    POST /actors
    '''

    def test_1a_add_actor_success_201(self):
        print('ADD AN ACTOR')
        response = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully added actor')
        self.assertEqual(data['actor']['name'], 'Steve Carell')

    def test_1b_add_actor_failure_400(self):
        response = self.client().post(
            '/actors',
            json=self.invalid_actor,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # RABC - Casting Assistant
    def test_1c_add_actor_failure_403_casting_assistant(self):
        response = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(
            data['message'], 'Access denied. Permission not found')

    '''
    POST /movies
    '''

    def test_2a_add_movie_success_201(self):
        print('ADD A MOVIE')
        response = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully added movie')
        self.assertEqual(data['movie']['title'], 'Hacksaw Ridge')

    def test_2b_add_movie_failure_400(self):
        response = self.client().post(
            '/movies',
            json=self.invalid_movie,
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # RABC - Casting Director
    def test_2c_add_movie_failure_403_casting_director(self):
        response = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(
            data['message'], 'Access denied. Permission not found')

    '''
    Get /actors
    '''

    def test_3a_get_all_actors_success_200(self):
        print('GET ACTOR')
        response = self.client().get(
            '/actors',
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actors successfully fetched')
        self.assertTrue(data['actors'])

    def test_3b_get_all_actors_failure_401(self):
        response = self.client().get(
            '/movies',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])

    '''
    Get /movies
    '''

    def test_4a_get_all_movies_success_200(self):
        print('GET MOVIE')
        response = self.client().get(
            '/movies',
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movies successfully fetched')
        self.assertTrue(data['movies'])

    def test_4b_get_all_movies_failure_401(self):
        response = self.client().get(
            '/movies',
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 401)
        self.assertTrue(data['message'])

    '''
    PATCH /actor/<int:id>
    '''

    def test_5a_update_actor_success_200(self):
        print('UPDATE ACTOR')
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Rainn Wilson'},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully updated actor details')
        self.assertEqual(data['actor']['name'], 'Rainn Wilson')

    def test_5b_update_actor_failure_400(self):
        response = self.client().patch(
            '/actors/1',
            json={},
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    '''
    PATCH /movie/<int:id>
    '''

    def test_6a_update_movie_success_200(self):
        print('UPDATE MOVIE')
        response = self.client().patch(
            '/movies/1',
            json={'title': 'Hacksaw Ridge'},
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully updated movie details')
        self.assertEqual(data['movie']['title'], 'Hacksaw Ridge')

    def test_6b_update_movie_failure_404(self):
        response = self.client().patch(
            '/movies/10',
            json={'title': 'Hacksaw Ridge'},
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'not found')

    # RABC - Casting Assistant
    def test_6c_update_movie_failure_403_casting_assistant(self):
        response = self.client().patch(
            '/movies/1',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(
            data['message'], 'Access denied. Permission not found')

    '''
    DELETE /actors/<int:id>
    '''

    def test_7a_delete_actor_success(self):
        print('DELETE ACTOR')
        response = self.client().delete(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully deleted actor')
        self.assertEqual(data['deleted_id'], 1)

    def test_7b_delete_actor_failure_404(self):
        response = self.client().delete(
            '/actors/10',
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    '''
    DELETE /movies/<int:id>
    '''

    def test_8a_delete_movie_success(self):
        print('DELETE MOVIE')
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'successfully deleted movie')
        self.assertEqual(data['deleted_id'], 1)

    def test_8b_delete_movie_failure_404(self):
        response = self.client().delete(
            '/movies/10',
            headers={"Authorization": f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    # RABC - Casting Director
    def test_8c_delete_movie_failure_403_casting_director(self):
        response = self.client().delete(
            '/movies/10',
            json=self.new_movie,
            headers={"Authorization": f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 403)
        self.assertEqual(
            data['message'], 'Access denied. Permission not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
