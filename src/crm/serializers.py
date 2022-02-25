from rest_framework import serializers

from .models import Client, Contract, Event
from accounts.models import User
from accounts.serializers import UserSerializer, UserSmallSerializer

import logging
# LOG
logger = logging.getLogger(__name__)

logger.warning('SERIALIZER')


# CLIENT
class ClientSerializer(serializers.ModelSerializer):
    client_manager = serializers.SlugRelatedField(slug_field='email', allow_null=True, queryset=User.objects.all())

    class Meta:
        model = Client
        fields = ['email', 'company_name', 'client_id', 'client_manager']
        extra_kwargs = {
            'email': {'write_only': True},
            'client_id': {'read_only': True},
            'lookup_field': 'client_id'
        }

    def validate(self, data):
        return data


class ClientDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email')
    client_manager = serializers.SlugRelatedField(slug_field='email', allow_null=True, queryset=User.objects.all())

    class Meta:
        model = Client
        fields = ['client_id', 'client_manager',
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


# CONTRACT

class ContractSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='company_name', queryset=Client.objects.all())
    contract_manager = serializers.SlugRelatedField(slug_field='email', allow_null=True, queryset=User.objects.all())

    class Meta:
        model = Contract
        fields = ['contract_id', 'title', 'client', 'contract_manager', 'status']

    def validate(self, data):
        return data


class ContractDetailSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='company_name', queryset=Client.objects.all())
    contract_manager = serializers.SlugRelatedField(slug_field='email', allow_null=True, queryset=User.objects.all())
    # status = serializers.SlugRelatedField(slug_field='email', queryset=Contract.objects.all())
    class Meta:
        model = Contract
        fields = ['title', 'client', 'contract_manager', 'status', 'contract_id', 'created_time', 'updating_time']
        extra_kwargs = {
            'created_time': {'read_only': True},
            'updating_time': {'read_only': True},
        }

    def validate(self, data):
        return data


# EVENT
class EventSerializer(serializers.ModelSerializer):
    contract = serializers.SlugRelatedField(slug_field='title', queryset=Contract.objects.all())
    event_manager = serializers.SlugRelatedField(slug_field='email', allow_null=True, queryset=User.objects.all())

    class Meta:
        model = Event
        fields = ['event_id', 'contract', 'event_manager', 'name']

    def validate(self, data):
        return data
