from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from api.models import Naver

from rest_framework import serializers


class NaverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Naver
        fields = ('birthdate', 'admission_date', 'job_role')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    naver = NaverSerializer()

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'naver')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        naver_data = validated_data.pop('naver')
        user = get_user_model().objects.create_user(**validated_data)
        Naver.objects.create(user=user, **naver_data)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and autheticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs