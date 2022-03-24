import pytest
from EpicEvents.settings import *

from .controllers import ApiTest


@pytest.mark.django_db(transaction=True)
def __test_signin_signout_view(client):
    api_test = ApiTest("vente_1@test.fr", "abcdef").launch_signin_signout()




