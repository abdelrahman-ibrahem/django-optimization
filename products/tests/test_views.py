import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db
class TestProductEndpoints:
    
    def test_top_products(self, auth_client, product_factory):
        client, user = auth_client
        category, _ = product_factory.create_batch(count=12, category_name="Appliances")
        
        url = reverse('top-products')
        
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        assert len(response.data) == 10
        
        assert response.data[0]['category_total_count'] == 12
        assert response.data[0]['category_name'] == "Appliances"