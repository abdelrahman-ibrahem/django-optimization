import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from products.models import Category, Product

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(db):
    user = User.objects.create_user(username="testuser", password="password123")
    token, _ = Token.objects.get_or_create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client, user

class ProductFactory:
    @staticmethod
    def create_batch(count=1, category_name="General", base_price=10.00):
        category = Category.objects.create(name=category_name)
        products = [
            Product.objects.create(
                name=f"Product {i}", 
                price=base_price + i, 
                category=category
            ) for i in range(count)
        ]
        return category, products

@pytest.fixture
def product_factory():
    return ProductFactory