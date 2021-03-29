from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@mail.com',
            password='pass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@mail.com',
            password='pass123',
            name='Name'
        )

    def test_users_listed(self):
        '''Happy path'''
        url = reverse('admin:api_core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        '''Happy path'''
        url = reverse('admin:api_core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_add_user_page(self):
        '''Happy path'''
        url = reverse('admin:api_core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
