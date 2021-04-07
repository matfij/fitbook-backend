from django.test import TestCase
from django.contrib.auth import get_user_model
from api_core import models


def sample_user(email='user@example.com', password='passq123'):
    '''Creates a sample user'''
    return get_user_model().objects.create_user(email, password)


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

    def test_super_user_created(self):
        '''Happy path'''
        email = 'admin@example.com'
        password = 'pass123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_admin)

    def test_tag_str(self):
        '''Test tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Gluten free"
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        '''Test ingredient string representation'''
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Tomato'
        )

        self.assertEqual(str(ingredient), ingredient.name)
