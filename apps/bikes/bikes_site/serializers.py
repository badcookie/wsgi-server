from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    """Processes list of products of manager's company."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'category_name')


class CategoryProductSerializer(serializers.ModelSerializer):
    """Processes list of products of manager's company for a particular category."""

    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category_name')


class PublicProductSerializer(serializers.ModelSerializer):
    """Processes list of all existing products."""

    company_name = serializers.CharField(source='company.name')

    class Meta:
        model = Product
        fields = ('name', 'description', 'company_name')


class PublicCategoryProductSerializer(serializers.ModelSerializer):
    """Processes list of all existing products for a particular category."""

    class Meta:
        model = Product
        fields = ('id', 'name', 'description')


class CategorySerializer(serializers.ModelSerializer):
    """Processes list of all existing categories."""

    class Meta:
        model = Category
        fields = '__all__'
