from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from api_core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTest(TestCase):
    '''Test publicly available ingredients endpoints'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTest(TestCase):
    '''Test private ingredients endpoints'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_ingredients_success(self):
        Ingredient.objects.create(user=self.user, name='Banana')
        Ingredient.objects.create(user=self.user, name='Pepper')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_assigned_to_creator(self):
        other_user = get_user_model().objects.create_user(
            email='other-user@example.com',
            password='other-pass123'
        )
        ingredient = Ingredient.objects.create(user=self.user, name='Banana')
        Ingredient.objects.create(user=other_user, name='Salt')
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def create_ingredient_success(self):
        payload = {'name': 'Goji'}
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def create_ingredient_invalid_name(self):
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status=status.HTTP_400_BAD_REQUEST)
