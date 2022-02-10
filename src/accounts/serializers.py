from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'user_id', 'password', 'role', 'confirm_password']
        extra_kwargs = {'email': {'read_only': True},
                        'role': {'read_only': True},
                        'password': {'write_only': True,
                                     'style': {'input_type': 'password'}},
                        'lookup_field': 'user_id'}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords not match")

        email = data["email"]
        users = User.objects.filter(email=email)
        if not users:
            return data
        else:
            raise serializers.ValidationError('This user already exist')