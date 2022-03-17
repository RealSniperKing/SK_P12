import pytest
from crm.models import Customer, Contract, Event
from accounts.models import User
from django.test import Client
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from EpicEvents.settings import *
from django.test.utils import override_settings
import json

# AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

# from django.test import Cliepythont
# client = Client()

# pytest -vv
# python -m pytest
# pytest -s
from rest_framework.reverse import reverse, reverse_lazy


def create_group_with_permissions(group_name, model, permissions_names_list):
    new_group, created = Group.objects.get_or_create(name=group_name)
    ct = ContentType.objects.get_for_model(model)

    for permission_name in permissions_names_list:
        codename = f'can_{permission_name}_{str(model.__name__).lower()}'
        permission = Permission.objects.create(
            codename=codename,
            name=f'can {permission_name} {str(model.__name__).lower()}'.capitalize(),
            content_type=ct)
        new_group.permissions.add(permission)
        print("permission code name = ", permission.codename)
        print("permission name = ", permission.name)
    return group_name


def create_user(user_email="vente_1@team.fr", user_password="abcdef", user_group_name="Equipe de vente"):
    # user = User(email=user_email, password=user_password)
    # user.save()
    user = User.objects.create(email=user_email, password=user_password)
    user.groups.add(Group.objects.get(name=user_group_name))
    return user

# router : add '-create" or '-list' suffix-detail




@pytest.mark.django_db(transaction=True)
def test_signin_view(client):
    # Build the URL
    url = reverse('api:signin-list')

    # Create group with permission
    customer_group_name = create_group_with_permissions("Equipe de vente", Customer, ["view", "add", "change", "delete"])

    # Add user in database
    user = create_user(user_email="vente_1@team.fr", user_group_name=customer_group_name)

    # Make a POST request to connect the user
    response = client.post(url, {'email': user.email, 'password': user.password})
    json_content = json.loads(response.content)

    # Verify that the response is correct
    assert response.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_users_view(client):
    url = reverse('api:signin-list')
    customer_group_name = create_group_with_permissions("Equipe de vente", Customer, ["view", "add", "change", "delete"])
    user = create_user(user_email="vente_1@team.fr", user_group_name=customer_group_name)

    response = client.post(url, {'email': user.email, 'password': user.password})
    json_content = json.loads(response.content)
    access_token = json_content["access"]
    csrftoken = response.cookies['csrftoken']
    # session_id = response.r
    print("csrftoken = ", csrftoken)
    assert response.status_code == 200

    url = reverse('api:clients-list')
    print("url = ", url)
    print("access = ", json_content["access"])
    #** {'HTTP_AUTHORIZATION': f'Bearer {json_content["access"]}'}
    response = client.get(url, headers={'X-CSRFToken': csrftoken,
                                        'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200