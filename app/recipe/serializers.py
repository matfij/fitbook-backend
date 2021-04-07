from rest_framework import serializers
from api_core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    '''Tag objects serializer'''

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
