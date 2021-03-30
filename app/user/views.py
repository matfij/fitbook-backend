from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    '''Exposes the create new user endpoint'''
    serializer_class = UserSerializer
