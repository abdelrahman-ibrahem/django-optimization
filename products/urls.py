from django.urls import path
from .views import TopProductsViewSet


urlpatterns = [
    path('top-products/', TopProductsViewSet.as_view(), name='top-products'),
]