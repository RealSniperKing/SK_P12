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