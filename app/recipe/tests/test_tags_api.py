from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from api_core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    '''Test publicly available tags endpoints'''

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    '''Test private tags endpoints'''

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags(self):
        Tag.objects.create(user=self.user, name='Vegetarian')
        Tag.objects.create(user=self.user, name='Dinner')
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_assigned_to_creator(self):
        other_user = get_user_model().objects.create_user(
            email='other-user@example.com',
            password='other-pass123'
        )
        Tag.objects.create(user=other_user, name='Vegetarian')
        tag = Tag.objects.create(user=self.user, name='Dinner')
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_success(self):
        payload = {'name': 'Fit'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid_name(self):
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
