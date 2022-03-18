import pytest
from crm.models import Customer, Contract, Event
from accounts.models import User
from django.test import Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from EpicEvents.settings import *
from django.test.utils import override_settings
import json
from .actions import create_group_with_permissions, create_user, Api
from api.utils_operations import permissions_from_admin_groups

# AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# from django.test import Cliepythont
# client = Client()

# pytest -vv
# python -m pytest
# pytest -s
from rest_framework.reverse import reverse, reverse_lazy

# router : add '-create" or '-list' suffix-detail


@pytest.mark.django_db(transaction=True)
def test_signin_view(client):
    api = Api("vente_1@test.fr", "abcdef")

    # Init database
    management_permissions = {"group_name": "Equipe de gestion", "permissions_list": [
        {"model": User, "permissions": ["view", "add", "change", "delete"]},
        {"model": Customer, "permissions": ["view", "add", "change", "delete"]},
        {"model": Contract, "permissions": ["view", "add", "change", "delete"]},
        {"model": Event, "permissions": ["view", "add", "change", "delete"]}
        ]}
    management_group_name = api.create_group_with_permissions(management_permissions)
    api.add_user_in_group(management_group_name)

    # Connection
    api.signin()

    # Get and test http method to current user
    api.view_model_access(User, "api:users")

    # Logout
    api.signout()

    # Build the URL
    # url = reverse('api:signin-list')
    #
    # # Create group with permission
    # customer_group_name = create_group_with_permissions("Equipe de vente", Customer, ["view", "add", "change", "delete"])
    #
    # # Add user in database
    # user = create_user(user_email="vente_1@team.fr", user_group_name=customer_group_name)
    #
    # # Make a POST request to connect the user
    # response = client.post(url, {'email': user.email, 'password': user.password})
    # json_content = json.loads(response.content)
    #
    # # Verify that the response is correct
    # assert response.status_code == 200


