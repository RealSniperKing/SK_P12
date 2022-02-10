from rest_framework import serializers

from .models import Client
from accounts.serializers import UserSerializer


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
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='email'
     )

    class Meta:
        model = Client
        fields = ['client_id',
                  'first_name', 'last_name', 'email', 'phone', 'mobile',
                  'company_name', 'address', 'address_complement', 'postal_code', 'city',
                  'author', 'created_time', 'updating_time',
                  'sales_contact'
                  ]
        extra_kwargs = {
            # 'author': {'read_only': True},
        }

    def validate(self, data):
        return data
