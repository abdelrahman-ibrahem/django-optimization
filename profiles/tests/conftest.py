import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
    return user

@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=test_user)
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    return client