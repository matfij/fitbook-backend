from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from api_core.models import Tag, Ingredient
from recipe import serializers


class BaseAttrViewSet(viewsets.ModelViewSet):
    '''Base ViewSet for recipe ViewSets'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(BaseAttrViewSet):
    '''Manages tags'''
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseAttrViewSet):
    '''Manages ingredients'''
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
