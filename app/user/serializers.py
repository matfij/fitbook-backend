from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as gettext
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 4}}

    def create(self, validated_data):
        '''Creates and returns a new user'''
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = gettext('Unable to authenticate')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs