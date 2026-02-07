from django.db import models
from django.db.models import OuterRef, Subquery, Count, Window, F
from django.db.models.functions import Rank


class ProductQuerySet(models.QuerySet):
    def with_category_stats(self):
        from .models import Category
        category_counts = Category.objects.filter(
            pk=OuterRef('category_id')
        ).annotate(
            total=Count('products')
        ).values('total')

        return self.annotate(
            category_total_count=Subquery(category_counts)
        )

    def top_10_per_category(self):
        ranked_queryset = self.annotate(
            rank=Window(
                expression=Rank(),
                partition_by=[F('category_id')],
                order_by=F('price').desc()
            )
        ).filter(
            rank__lte=10
        ).with_category_stats()

        return ranked_queryset

    def get_optimized_top_products(self):
        return self.select_related('category').top_10_per_category()