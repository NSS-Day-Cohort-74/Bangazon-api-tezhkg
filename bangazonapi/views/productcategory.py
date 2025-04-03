"""
   Author: Daniel Krusch
   Purpose: To convert product category data to json
   Methods: GET, POST
"""

"""View module for handling requests about product categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductCategory
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .product import ProductSerializer


class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product category"""
    products = serializers.SerializerMethodField()

    class Meta:
        model = ProductCategory
        url = serializers.HyperlinkedIdentityField(
            view_name='productcategory',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'products')
        depth = 1

    def get_products(self, obj):
        products = obj.products.order_by('-id')[:5]
        return ProductSerializer(products, many=True).data
    

class ProductCategories(ViewSet):
    """Categories for products"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_product_category = ProductCategory()
        new_product_category.name = request.data["name"]
        new_product_category.save()

        serializer = ProductCategorySerializer(new_product_category, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category"""
        try:
            category = ProductCategory.objects.get(pk=pk)
            serializer = ProductCategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to ProductCategory resource"""
        product_category = ProductCategory.objects.all()

        # Support filtering ProductCategorys by area id
        # name = self.request.query_params.get('name', None)
        # if name is not None:
        #     ProductCategories = ProductCategories.filter(name=name)

        serializer = ProductCategorySerializer(
            product_category, many=True, context={'request': request})
        return Response(serializer.data)
