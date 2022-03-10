from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User
from django.contrib.auth.models import Group


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
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
        if user is None:
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
    #client_manager = serializers.SlugRelatedField(slug_field='email', allow_null=True, queryset=User.objects.all())
    # groups = serializers.SlugRelatedField(slug_field='name', allow_null=True, queryset=Group.objects.all())
    # groups = serializers.SlugRelatedField(slug_field='name', allow_null=True, queryset=Group.objects.all())
    # groups = serializers.SlugRelatedField(many=True, slug_field='name', allow_null=True, queryset=Group.objects.all())
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    # group_name = serializers.SlugRelatedField(slug_field='name', write_only=True, allow_null=True, queryset=Group.objects.all())

    class Meta:
        model = User
        fields = ['email', 'user_id', 'password', 'role', 'confirm_password', 'groups']
        extra_kwargs = {'email': {'read_only': True},
                        'password': {'write_only': True,
                                     'style': {'input_type': 'password'}},
                        'lookup_field': 'user_id'}
    print("-------+++++")

    def validate(self, data):
        # Passwords matching ?
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords not match")

        # Check if the user exist
        email = data["email"]
        users = User.objects.filter(email=email)
        if users.exists():
            raise serializers.ValidationError('This user already exist')

        # Check if the group_name exist
        # role = data["role"]
        # if role:
        #     group_ob = Group.objects.filter(name=role)
        #     if not group_ob:
        #         raise serializers.ValidationError('Invalid group name')

        # group_ob = Group.objects.filter(name=group_name)
        # if not group_ob:
        #     raise serializers.ValidationError('Instance not found')

        return data


class UserDetailSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = ['email', 'user_id', 'role', 'groups']
        extra_kwargs = {'groups': {'read_only': True}}

    def validate(self, data):
        return data

