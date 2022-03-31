import pytest
from crm.models import Customer, Contract, Event
from accounts.models import User
from django.test import Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from EpicEvents.settings import *
from django.test.utils import override_settings
import json
from .models import Api
from .controllers import ApiTest


@pytest.mark.django_db(transaction=True)
def test_views_permissions_true():
    api_test = ApiTest("gestion_1@test.fr", "abcdef")

    # Init database
    group_name = "Equipe de gestion"
    management_permissions = {"group_name": group_name, "permissions_list": [
        {"model": User, "permissions": ["view", "add", "change", "delete"]},
        {"model": Customer, "permissions": ["view", "add", "change", "delete"]},
        {"model": Contract, "permissions": ["view", "add", "change", "delete"]},
        {"model": Event, "permissions": ["view", "add", "change", "delete"]}
    ]}
    api_test.assign_permissions_to_user(management_permissions, group_name)
    api_test.set_management_group_name("Equipe de gestion")

    # USERS URL
    crud_actions = {"create": 200, "read-list": 200, "read-detail": 200, "update": 200, "delete": 200}
    api_test.launch_user_crud_actions("users", crud_actions)

    # CLIENTS URL
    crud_actions = {"create": 200, "read-list": 200, "read-detail": 200, "update": 200, "delete": 200}
    api_test.launch_customer_crud_actions("clients", crud_actions)

    # CONTRACT URL
    crud_actions = {"create": 200, "read-list": 200, "read-detail": 200, "update": 200, "delete": 200}
    api_test.launch_contract_crud_actions("contracts", crud_actions)

    # EVENT URL
    crud_actions = {"create": 200, "read-list": 200, "read-detail": 200, "update": 200, "delete": 200}
    api_test.launch_event_crud_actions("events", crud_actions)


@pytest.mark.django_db(transaction=True)
def __test_views_permissions_false():
    api_test = ApiTest("gestion_1@test.fr", "abcdef")

    # Init database
    group_name = "Equipe de gestion"
    management_permissions = {"group_name": group_name, "permissions_list": [
        {"model": User, "permissions": []},
        {"model": Contract, "permissions": []},
        {"model": Customer, "permissions": []},
        {"model": Event, "permissions": []}
    ]}
    api_test.assign_permissions_to_user(management_permissions, group_name)

    crud_actions = {"create": 405, "read-list": 405, "read-detail": 405, "update": 405, "delete": 405}
    api_test.launch_user_crud_actions("users", crud_actions)
    api_test.launch_crud_actions("clients", crud_actions)
    api_test.launch_crud_actions("contracts", crud_actions)
    api_test.launch_crud_actions("events", crud_actions)
