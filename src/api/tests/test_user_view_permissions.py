import pytest
from crm.models import Customer, Contract, Event
from accounts.models import User
from django.test import Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from EpicEvents.settings import *
from django.test.utils import override_settings
import json
from .actions import Api, launch_crud_actions


@pytest.mark.django_db(transaction=True)
def test_user_view_permissions_true():
    api = Api("vente_1@test.fr", "abcdef")

    # Init database
    group_name = "Equipe de gestion"
    management_permissions = {"group_name": group_name, "permissions_list": [
        {"model": User, "permissions": ["view", "add", "change", "delete"]},
        {"model": Contract, "permissions": ["view", "add", "change", "delete"]},
        {"model": Customer, "permissions": ["view", "add", "change", "delete"]},
        {"model": Event, "permissions": ["view", "add", "change", "delete"]}
    ]}
    api.create_group_with_permissions(management_permissions)
    api.add_user_in_group(group_name)

    crud_actions = {"create": 200, "read": 200, "update": 200, "delete": 200}
    launch_crud_actions(api, "users", crud_actions)


@pytest.mark.django_db(transaction=True)
def test_user_view_permissions_false():
    api = Api("vente_1@test.fr", "abcdef")

    # Init database
    group_name = "Equipe de gestion"
    management_permissions = {"group_name": group_name, "permissions_list": [
        {"model": User, "permissions": []},
        {"model": Contract, "permissions": []},
        {"model": Customer, "permissions": []},
        {"model": Event, "permissions": []}
    ]}
    api.create_group_with_permissions(management_permissions)
    api.add_user_in_group(group_name)

    crud_actions = {"create": 405, "read": 405, "update": 405, "delete": 405}
    launch_crud_actions(api, "users", crud_actions)
