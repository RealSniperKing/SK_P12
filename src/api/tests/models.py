from accounts.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from EpicEvents.settings import *
from rest_framework.reverse import reverse

from django.test import Client
import json
from accounts.models import ManagementGroupName


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
        # Build the URL
        url = reverse('api:signin-list')

        # Make a POST request to connect the user
        response = self.client.post(url, {'email': self.email, 'password': self.password})
        assert response.status_code == 200

        json_content = json.loads(response.content)
        self.access_token = json_content["access"]

    def read_kwargs(self, kwargs):
        user_id = kwargs.get('user_id', "0")
        client_id = kwargs.get('client_id', "0")
        contract_id = kwargs.get('contract_id', "0")
        event_id = kwargs.get('event_id', "0")
        data = kwargs.get('data', {})
        return user_id, client_id, contract_id, event_id, data

    def detail_url_from_kwargs(self, view_url, kwargs_values):
        user_id, client_id, contract_id, event_id, data = self.read_kwargs(kwargs_values)
        url = "bad"
        if user_id != "0":
            url = reverse(view_url, kwargs={"user_id": user_id})
        if client_id != "0":
            url = reverse(view_url, kwargs={"client_id": client_id})
        if contract_id != "0":
            url = reverse(view_url, kwargs={"contract_id": contract_id})
        if event_id != "0":
            url = reverse(view_url, kwargs={"event_id": event_id})
        return url, data

    def view_get(self, view_url, expected_status_code, **kwargs):
        if "-detail" in view_url:
            url, _ = self.detail_url_from_kwargs(view_url, kwargs)
        else:
            url = reverse(view_url)
        response = self.client.get(url,
                                   format='json',
                                   **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'},
                                   follow=True)
        assert response.status_code == expected_status_code

        status_codes = [200, 400]
        if response.status_code in status_codes:
            json_content = json.loads(response.content)
            if "-detail" in view_url:
                assert json_content is not {}
            else:
                assert json_content["results"]["success"] is True

    def view_post(self, view_url, expected_status_code, **kwargs):
        data = kwargs.get('data', {})

        url = reverse(view_url)

        response = self.client.post(url,
                                    data=data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})

        assert response.status_code == expected_status_code

        json_content = {}
        status_codes = [200, 400]
        if response.status_code in status_codes:
            json_content = json.loads(response.content)
            assert json_content["success"] is True
        return json_content

    def view_put(self, view_url, expected_status_code, **kwargs):
        url, data = self.detail_url_from_kwargs(view_url, kwargs)

        response = self.client.put(url,
                                   data=data,
                                   content_type='application/json',
                                   format='json',
                                   **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})
        assert response.status_code == expected_status_code

        status_codes = [200, 400]
        if response.status_code in status_codes:
            json_content = json.loads(response.content)
            assert json_content["success"] is True

    def view_delete(self, view_url, expected_status_code, **kwargs):
        url, data = self.detail_url_from_kwargs(view_url, kwargs)
        response = self.client.delete(url,
                                      content_type='application/json',
                                      format='json',
                                      **{'HTTP_AUTHORIZATION': f'Bearer {self.access_token}'})
        assert response.status_code == expected_status_code

        status_codes = [200, 400]
        if response.status_code in status_codes:
            json_content = json.loads(response.content)
            assert json_content["success"] is True

    def create_group_with_permissions(self, groupname_models_permissionslist):
        group_name = groupname_models_permissionslist["group_name"]
        models_and_permissions_list = groupname_models_permissionslist["permissions_list"]

        new_group, created = Group.objects.get_or_create(name=group_name)

        for model_and_permissions in models_and_permissions_list:
            model = model_and_permissions["model"]
            permissions = model_and_permissions["permissions"]

            for permission_name in permissions:
                codename = f'{permission_name}_{str(model.__name__).lower()}'

                # Get permission
                permission = Permission.objects.filter(codename=codename).first()
                if permission:
                    new_group.permissions.add(permission)

        return group_name

    def add_user_in_group(self, user_group_name):
        if self.current_user:
            my_group = Group.objects.get(name=user_group_name)
            my_group.user_set.add(self.current_user)

    def signout(self):
        url = reverse('api:signout')
        response = self.client.get(url)
        assert response.status_code == 200
