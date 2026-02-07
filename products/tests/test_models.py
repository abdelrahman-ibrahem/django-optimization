import pytest
from products.models import Product

pytestmark = pytest.mark.django_db

class TestProductModels:
    def test_product_creation(self, product_factory):
        category, products = product_factory.create_batch(count=5, category_name="Electronics")
        
        assert Product.objects.count() == 5
        assert products[0].category.name == "Electronics"
        
    def test_product_str(self, product_factory):
        _, products = product_factory.create_batch(count=1)
        assert str(products[0]) == "Product 0"