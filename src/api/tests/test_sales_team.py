import pytest
from crm.models import Customer, Contract, Event
from accounts.models import User
from EpicEvents.settings import *
from .controllers import ApiTest


@pytest.mark.django_db(transaction=True)
def test_sales_team_permissions_true():
    api_test = ApiTest("gestion_1@test.fr", "pwTEST?_741.")

    # Init database
    group_name = "Equipe de vente"
    management_permissions = {"group_name": group_name, "permissions_list": [
        {"model": User, "permissions": []},
        {"model": Customer, "permissions": ["view", "add", "change", "delete"]},
        {"model": Contract, "permissions": ["view", "add", "change", "delete"]},
        {"model": Event, "permissions": ["view", "add"]}
    ]}
    api_test.assign_permissions_to_user(management_permissions, group_name)
    api_test.set_management_group_name("Equipe de gestion")

    # USERS URL
    crud_actions = {"create": 405, "read-list": 405, "read-detail": 404, "update": 404, "delete": 404}
    api_test.launch_user_crud_actions("users", crud_actions)


@pytest.mark.django_db(transaction=True)
def __test_views_permissions_false():
    api_test = ApiTest("gestion_1@test.fr", "pwTEST?_741.")

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
