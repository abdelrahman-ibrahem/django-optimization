from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class TopProductsViewSet(generics.ListAPIView):
    queryset = Product.objects.get_optimized_top_products()
    serializer_class = ProductSerializer
