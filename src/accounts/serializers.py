from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User
from django.contrib.auth.models import Group


# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)
logger.error("------------------")

# CONNECTION
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
    email = serializers.EmailField(required=True)  #allow_blank=True
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    def validate(self, data):
        logger.error(data)
        email = data['email']
        password = data['password']
        logger.error(User.objects.all())
        user_temp = User.objects.filter(email=email).first()
        logger.error(f"user_temp = {user_temp}")
        logger.error(f'User.objects.filter(email=email).exists() = {User.objects.filter(email=email).exists()}')

        user = authenticate(username=email, password=password)
        if user is None:
            logger.error(f'user = {user}')
            raise serializers.ValidationError('Bad email or password')
        return data


# USER
class UserSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, allow_blank=False, write_only=True)
    groups = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['email', 'user_id', 'password', 'confirm_password', 'groups']
        extra_kwargs = {'email': {'read_only': True},
                        'password': {'write_only': True,
                                     'style': {'input_type': 'password'}},
                        'lookup_field': 'user_id'}
    print("-------+++++")

    def validate(self, data):
        # Is it a valid password ?
        password = data['password']
        validate_password(password)

        # Passwords matching ?
        if password != data['confirm_password']:
            raise serializers.ValidationError("passwords not match")

        # Check if the user exist
        email = data["email"]
        users = User.objects.filter(email=email)
        if users.exists():
            raise serializers.ValidationError('This user already exist')

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

    def validate(self, data):
        return data


class UserDetailSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='name', allow_empty=True, required=False, queryset=Group.objects.all())
    confirm_password = serializers.CharField(style={'input_type': 'password'}, allow_blank=False, write_only=True)
    # email = serializers.EmailField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'user_id', 'groups', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True,
                                     'style': {'input_type': 'password'}}}

    def validate(self, data):
        # Is it a valid password ?
        password = data['password']
        validate_password(password)

        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords not match")

        return data

