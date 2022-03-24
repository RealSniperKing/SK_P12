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
def test_signin_signout_view(client):
    api = Api("vente_1@test.fr", "abcdef")

    # Connection
    api.signin()

    # Logout
    api.signout()


