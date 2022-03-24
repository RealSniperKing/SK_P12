from accounts.models import User
from crm.models import Customer
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from EpicEvents.settings import *
from django.conf import settings
from rest_framework.reverse import reverse, reverse_lazy

from rest_framework.test import APIRequestFactory
from django.test import Client
import json
from api.utils_operations import permissions_from_admin_groups


class Api:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.current_user = self.create_user()
        self.client = Client()
        self.access_token = None

    def create_user(self, user_email=None, password=None):
        if user_email is None or password is None:
            user = User.objects.create_user(email=self.email, password=self.password)
            user.save()
        else:
            user = User.objects.create_user(email=user_email, password=password)
            user.save()
        return user

    def signin(self):
        print("SIGNIN")
        # Build the URL
        url = reverse('api:signin-list')

        # Make a POST request to connect the user
        response = self.client.post(url, {'email': self.email, 'password': self.password})
        print("response.status_code = ", response.status_code)
        assert response.status_code == 200

        json_content = json.loads(response.content)
        self.access_token = json_content["access"]

    def view_get(self, view_url, expected_status_code, **kwargs):
        print("VIEW GET")

        if "-detail" in view_url:
            user_id = kwargs.get('user_id', "0")
            url = reverse(view_url, kwargs={"user_id": user_id})
        else:
            url = reverse(view_url)
        response = self.client.get(url,
                                   format='json',
                                   **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'},
                                   follow=True)
        print(response.status_code)
        assert response.status_code == expected_status_code
        print("response.content = ", response.content)

    def view_post(self, view_url, expected_status_code, **kwargs):
        print("VIEW POST")
        data = kwargs.get('data', {})

        json_content = {}
        url = reverse(view_url)

        response = self.client.post(url,
                                    data=data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})

        # print(response.status_code)
        # print(response.content)
        assert response.status_code == expected_status_code
        json_content = json.loads(response.content)
        # print("json_content = ", json_content)
        return json_content

    def view_put(self, view_url, expected_status_code, **kwargs):
        print("VIEW PUT")

        user_id = kwargs.get('user_id', "0")
        data = kwargs.get('data', {})

        url = reverse(view_url, kwargs={"user_id": user_id})
        response = self.client.put(url,
                                   data=data,
                                   content_type='application/json',
                                   format='json',
                                   **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})
        print(response)
        print("response.content = ", response.content)
        json_content = json.loads(response.content)
        assert response.status_code == expected_status_code

    def view_delete(self, view_url, expected_status_code, **kwargs):
        print("VIEW PUT")

        user_id = kwargs.get('user_id', "0")

        url = reverse(view_url, kwargs={"user_id": user_id})
        response = self.client.delete(url,
                                      content_type='application/json',
                                      format='json',
                                      **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})
        print(response.status_code)
        print("response.content = ", response.content)
        assert response.status_code == expected_status_code

    def create_group_with_permissions(self, groupname_models_permissionslist):
        group_name = groupname_models_permissionslist["group_name"]
        models_and_permissions_list = groupname_models_permissionslist["permissions_list"]

        new_group, created = Group.objects.get_or_create(name=group_name)

        for model_and_permissions in models_and_permissions_list:
            model = model_and_permissions["model"]
            permissions = model_and_permissions["permissions"]

            content_type = ContentType.objects.get_for_model(model)
            print("............")
            for permission_name in permissions:
                codename = f'{permission_name}_{str(model.__name__).lower()}'
                name = f'{permission_name} {str(model.__name__).lower()}'.capitalize()

                # permission = Permission.objects.create(
                #     codename=codename,
                #     name=name,
                #     content_type=content_type)

                # Get permission
                permission = Permission.objects.filter(codename=codename).first()
                # print("permission = ", permission)
                if permission:
                    new_group.permissions.add(permission)

        return group_name

    def add_user_in_group(self, user_group_name):
        if self.current_user:
            self.current_user.groups.clear()
            self.current_user.groups.add(Group.objects.get(name=user_group_name))

    def signout(self):
        url = reverse('api:signout')
        response = self.client.get(url)
        assert response.status_code == 200





def create_group_with_permissions(group_name, model, permissions_names_list):
    new_group, created = Group.objects.get_or_create(name=group_name)
    content_type = ContentType.objects.get_for_model(model)
    # content_type = ContentType.objects.get_for_model(settings.AUTH_USER_MODEL)
    print("............")
    for permission_name in permissions_names_list:
        codename = f'{permission_name}_{str(model.__name__).lower()}'
        name = f'{permission_name} {str(model.__name__).lower()}'.capitalize()
        # print("permission code name = ", codename)
        # print("permission name = ", name)

        # permission = Permission.objects.create(
        #     codename=codename,
        #     name=name,
        #     content_type=content_type)

        # Get permission
        permission = Permission.objects.filter(codename=codename).first()
        # print("permission = ", permission)
        if permission:
            new_group.permissions.add(permission)

    return group_name


def create_user(user_email="vente_1@team.fr", user_password="abcdef", user_group_name="Equipe de vente"):
    # user = User(email=user_email, password=user_password)
    # user.save()
    user = User.objects.create(email=user_email, password=user_password)
    user.groups.add(Group.objects.get(name=user_group_name))
    return user


def create_client(email="client@test.fr", company_name="Test_1_company"):
    customer = Customer.objects.create(email=email, company_name=company_name)
    return customer