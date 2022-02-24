from rest_framework import serializers

from .models import Client
from accounts.serializers import UserSerializer, UserSmallSerializer


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email', 'company_name', 'client_id']
        extra_kwargs = {
            'email': {'write_only': True},
            'client_id': {'read_only': True},
            'lookup_field': 'client_id'
        }

    def validate(self, data):
        return data


class ClientDetailSerializer(serializers.ModelSerializer):
    # author = UserSerializer(many=False, read_only=True).get_fields()['email']
    # sales_contact = UserSerializer(many=False, read_only=True).get_fields()['email']
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    # author = UserSmallSerializer(many=False, read_only=True)
    # sales_contact = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    # sales_contact = UserSmallSerializer(many=False, read_only=False)

    class Meta:
        model = Client
        fields = ['client_id',
                  'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'address', 'address_complement', 'postal_code', 'city',
                  'author', 'created_time', 'updating_time',
                  'sales_contact'
                  ]
        extra_kwargs = {
            'updating_time': {'read_only': True},
        }

    def validate(self, data):
        return data
