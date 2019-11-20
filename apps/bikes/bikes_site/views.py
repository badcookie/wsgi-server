from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Product, Manager, Category
from .serializers import (
    ProductSerializer,
    CategoryProductSerializer,
    PublicProductSerializer,
    PublicCategoryProductSerializer,
    CategorySerializer,
)


class PublicProductListPagination(PageNumberPagination):
    page_size = 5


class CategoriesViewSet(viewsets.ModelViewSet):
    """Allows to get a list of all existing categories."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    """Defines actions and queries accessible to managers only."""

    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        return (
            CategoryProductSerializer
            if self.kwargs.get('category_id') is not None
            else ProductSerializer
        )

    def get_queryset(self):
        manager = Manager.objects.get(user=self.request.user)
        company_products = Product.objects.filter(company=manager.company)

        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            category = get_object_or_404(Category, id=category_id)
            category_products = company_products.filter(category=category)
            return category_products

        return company_products

    def get_object(self):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(self.get_queryset(), id=product_id)
        return product

    def perform_create(self, serializer):
        category_id = self.request.data['category']
        category = get_object_or_404(Category, id=category_id)
        manager = Manager.objects.get(user=self.request.user)
        serializer.save(company=manager.company, category=category)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        fields_to_update = request.data
        for field, value in fields_to_update.items():
            setattr(product, field, value)
        product.save()
        updated_product = self.get_serializer(product).data
        return Response(updated_product)


class PublicProductViewSet(viewsets.ModelViewSet):
    """Defines actions and queries accessible to all users."""

    permission_classes = (permissions.AllowAny,)
    pagination_class = PublicProductListPagination

    def get_object(self):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        return product

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id is not None:
            category = get_object_or_404(Category, id=category_id)
            category_products = Product.objects.filter(category=category)
            return category_products

        return Product.objects.all()

    def get_serializer_class(self):
        return (
            PublicCategoryProductSerializer
            if self.kwargs.get('category_id') is not None
            else PublicProductSerializer
        )
