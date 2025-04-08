from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bangazonapi.models import ProductLike
from rest_framework import status
from .product import ProductSerializer
from .profile import CustomerSerializer




class ProductLikeSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer(many=True)

    class Meta:
        model = ProductLike
        fields = ('id', 'product', 'customer')

# class ProductLikes(ViewSet):

#     permission_classes = (IsAuthenticatedOrReadOnly,)

#     def create(self, request):

#         new_product_like = ProductLike()
#         new_product_like = request.data["product"]
#         new_product_like.save()

#         serializer = ProductLikeSerializer(new_product_like, context={'request': request})

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def list(self, request):
#         product_like = ProductLike.objects.all()


#         serializer = ProductLikeSerializer(
#             product_like, many=True, context={'request': request})
#         return Response(serializer.data)
    
#     # def destroy(self, request, pk=None):
#     #     product_like = ProductLike.
    