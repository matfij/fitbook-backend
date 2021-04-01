from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    '''Tests not-authenticated users'''

    def setUp(self):
        self.client = APIClient()

    def test_user_created_success(self):
        '''Happy path'''
        payload = {
            'email': 'user@example.com',
            'password': 'pass123',
            'name': 'Johann'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('pass123', res.data)

    def test_user_exists(self):
        '''Fail to create duplicate user'''
        payload = {
            'email': 'user@example.com',
            'password': 'pass123',
            'name': 'Johann'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        '''Check if password length is sufficient'''
        payload = {
            'email': 'user@example.com',
            'password': 'pas',
            'name': 'Johann'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_token(self):
        '''Happy path'''
        payload = {
            'email': 'user@example.com',
            'password': 'pass123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_token_fail_wrong_credentials(self):
        '''Fail to crate token with invalid credentials'''
        create_user(email='user@example.com', password='pass123')
        payload = {
            'email': 'user@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_token_fail_no_user(self):
        '''Fail to crate token with user no'''
        payload = {
            'email': 'user@example.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)