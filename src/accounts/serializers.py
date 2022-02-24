from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class SignupSerializer(ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True, 'style': {'input_type': 'password'}}
                        }

    def validate(self, data):
        # https://www.django-rest-framework.org/api-guide/fields/#core-arguments
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords not match")
        return data


class SigninSerializer(serializers.Serializer):
    """Use serializers.Serializer to lose models.EmailField(unique=True"""
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError('Bad email or password')
        return data


class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'user_id', 'password', 'role', 'confirm_password', 'groups']
        extra_kwargs = {'email': {'read_only': True},
                        'password': {'write_only': True,
                                     'style': {'input_type': 'password'}},
                        'lookup_field': 'user_id'}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords not match")
        # return data
        email = data["email"]
        users = User.objects.filter(email=email)
        if not users:
            return data
        else:
            raise serializers.ValidationError('This user already exist')


class UserPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'user_id', 'role', 'groups']
        extra_kwargs = {'groups': {'read_only': True}}

    def validate(self, data):
        return data
