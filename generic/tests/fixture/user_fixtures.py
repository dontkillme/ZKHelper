import pytest
from generic.tests.factory.user_factory import UserFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture(name="regular_user")
def create_regular_user():
    return UserFactory.create()


@pytest.fixture(name="regular_user_2")
def create_regular_user_2():
    return UserFactory.create()


@pytest.fixture(name="apiclient_with_token")
def create_apiclient_with_token(regular_user):
    token, _ = Token.objects.get_or_create(user=regular_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client


@pytest.fixture(name="apiclient_2_with_token")
def create_apiclient_2_with_token(regular_user_2):
    token, _ = Token.objects.get_or_create(user=regular_user_2)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client
