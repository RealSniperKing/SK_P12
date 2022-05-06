from accounts.models import User
from crm.models import Customer
from django.contrib.auth.models import Group, Permission
from EpicEvents.settings import *


def create_group_with_permissions(group_name, model, permissions_names_list):
    new_group, created = Group.objects.get_or_create(name=group_name)
    for permission_name in permissions_names_list:
        codename = f'{permission_name}_{str(model.__name__).lower()}'

        # Get permission
        permission = Permission.objects.filter(codename=codename).first()
        if permission:
            new_group.permissions.add(permission)

    return group_name


def create_user(user_email="vente_1@team.fr", user_password="abcdef", user_group_name="Equipe de vente"):
    user = User.objects.create(email=user_email, password=user_password)
    user.groups.add(Group.objects.get(name=user_group_name))
    return user


def create_client(email="client@test.fr", company_name="Test_1_company"):
    customer = Customer.objects.create(email=email, company_name=company_name)
    return customer
