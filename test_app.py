import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor


CASTING_ASSISTANT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxZaUNIYmhvSG1tNXVvbWNfU3BFNiJ9.eyJpc3MiOiJodHRwczovL2F1dGgtbWFuc291ci51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDkwOTQyMDMzMTcxMjc5ODI5MjgiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2F1dGgtbWFuc291ci51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTkzMzgwODI2LCJleHAiOjE1OTM0NjcyMjUsImF6cCI6IjhLREdORG52TUxyWGxlaTZ6Znk0REUxV1l5TzN4RlB0Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.FwYN8TaL4o4sg-dt7ZhMuUcgRnIMmao8JP65Ph9_MAB9ZuH_Orq7Y9_dpOCtDPZrYXGZyvjBxKs4UEIOLk-HGz8qcHFtpZ0RercfMd4MjziFQjqisNMU9yIi4D1psSPJhZIlIIIVlrVF9ZuV1QRnS5lH3ROSI1EiUm4QxDo4vJPIqCpd8D-3UV9WrkhUWnBlpAmcIi9k-Y0nAQBgMiEW32rNChMPnUAAkMvI-Oi3z7NXh4e_069NxEt9FgFaXUG79h8qT_Z4dQD3ntPj29SJV1j8Dx06xgyiSU6kR_3lWeswU7g9brieDTTES3HP7ZX-2uHEINY9isFUuopecqDiWA'   
CASTING_DIRECTOR = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxZaUNIYmhvSG1tNXVvbWNfU3BFNiJ9.eyJpc3MiOiJodHRwczovL2F1dGgtbWFuc291ci51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTM3MTQ5ODM5Mjg2ODE3NDE0MzAiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2F1dGgtbWFuc291ci51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTkzMzgwNDkwLCJleHAiOjE1OTM0NjY4ODksImF6cCI6IjhLREdORG52TUxyWGxlaTZ6Znk0REUxV1l5TzN4RlB0Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.QxC7F8Nw9vo4vmnzSscuVx3tWxn_u2XVzTemKux-9u8QM3ronmSTOwfCNwMM6fTgNQDQvp2NFOd6x1RK3xp8ZvC2DzLnubELL8wYhSATHzFq_iDuLUVvGEN4nX3IUPh03tWMnx2bGbj8c4KP5iq3sEt-AsPiOx5CJjLWTZsXWpTHkHhVT6zy-qGnN781HW6GcA1cnb7vEI8m3Ke9CB9wlDW2mp44A0qFy-8XZB0fapEZQepqqosIDiqEKml9eARuXChstMUwld9R-xPbmEuKOAsi61HeJNdAN7G9_7c_TTd-KgTWHSI7UVN-S_FScdHW5OYJfEQfpMOWymnlr1EC_w' 
EXECUTIVE_PRODUCER = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImxZaUNIYmhvSG1tNXVvbWNfU3BFNiJ9.eyJpc3MiOiJodHRwczovL2F1dGgtbWFuc291ci51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDg3MTY2NDExODQ2MTYxMjQ2MTEiLCJhdWQiOlsiY2FzdGluZy1hZ2VuY3kiLCJodHRwczovL2F1dGgtbWFuc291ci51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTkzMzgwMjQyLCJleHAiOjE1OTM0NjY2NDEsImF6cCI6IjhLREdORG52TUxyWGxlaTZ6Znk0REUxV1l5TzN4RlB0Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.NrNGhnAy593XhxqWQILqWC6gZL2-_CWNkzwtefnqSxkche_Q3q7XMjG41z06jVSUrazrubk_M68ZCVVeh2tKpZjqrmky2V_lJH311Fd726siTtIikuDJ93qc1-NGSaPyZfjB-Md3RAv2ml1OQyKMaIXuwEt88-VlUcmlNUZvGW_iHabLGFVadmq_woTDV4PLYNN5HPeYc94vsjZNKvxcO1O3aN65Ab0K46JzhELmrp4cSQ16s7RzXBWTQrAU9INNtK53uDimV3ZzqdimpxWJeUjcQDsvsXqg0bKLG6EtT5fngL8cBVOcI11VDFlNoZozYTLu5tFFc96i0_8zz3syFA' 

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
