from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_success(self):
        '''Happy path'''
        email = 'user@example.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_fail_email_value(self):
        '''Should fail to create user with email not provided'''
        with self.assertRaises(ValueError):
            email = None
            password = 'pass123'
            get_user_model().objects.create_user(
                    email=email,
                    password=password
                )

    def test_admin_created(self):
        '''Happy path'''
        email = 'admin@example.com'
        password = 'pass123'
        user = get_user_model().objects.create_admin(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)
