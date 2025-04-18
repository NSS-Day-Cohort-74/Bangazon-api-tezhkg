from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bangazonapi.models import Customer, Product, Store, OrderProduct, Favorite
from .product import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    store_products = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    sold_products = serializers.SerializerMethodField()
    name_of_owner = serializers.SerializerMethodField()


    class Meta:
        model = Store
        fields = (
            "id",
            "name",
            "description",
            "owner",
            "size",
            "store_products",
            "sold_products",
            "name_of_owner",
        )
        depth = 1

    def get_store_products(self, obj):
        products = obj.owner.products.all()
        return ProductSerializer(products, many=True).data

    def get_sold_products(self, obj):
        owner_id = obj.owner.id

        all_products = OrderProduct.objects.filter(
            product__customer_id=owner_id, order__payment_type__isnull=False
        )
        sold_products = []

        for product in all_products:
            if product.product not in sold_products:
                sold_products.append(product.product)

        return ProductSerializer(sold_products, many=True).data

    def get_size(self, obj):
        count_of_products = obj.owner.products.count()
        return count_of_products
    
    def get_name_of_owner(self, obj):
        user = obj.owner.user
        first_name = user.first_name if user.first_name else ""
        last_name = user.last_name if user.last_name else ""
        if first_name == "" and last_name == "":
            return user.username
        
        return f"{first_name} {last_name}".strip()
    
class StoreDetailSerializer(StoreSerializer):
    is_favorite = serializers.SerializerMethodField()

    class Meta(StoreSerializer.Meta):
        fields = StoreSerializer.Meta.fields + ("is_favorite", "favorites")

    
    def get_is_favorite(self, obj):
        request = self.context.get("request")

        current_user = Customer.objects.get(user=request.auth.user)

        is_it_favorite = Favorite.objects.filter(customer=current_user, store=obj.pk).exists()

        return is_it_favorite


class Stores(ViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        current_user = Customer.objects.get(user=request.auth.user)

        if Store.objects.filter(owner=current_user).exists():
            return Response(
                {"message": "store already exists for this owner."},
                status=status.HTTP_409_CONFLICT,
            )

        new_store = Store()
        new_store.name = request.data["name"]
        new_store.description = request.data["description"]
        # owner is coming in as the request.auth.user
        # get user
        user = request.auth.user
        # set customer to user
        customer = Customer.objects.get(user=user)
        # set owner of the store to customer
        new_store.owner = customer
        # set the customer

        new_store.save()

        serializer = StoreSerializer(new_store, context={"request": request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):

        stores = Store.objects.all()
        serializer = StoreSerializer(stores, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            store = Store.objects.get(pk=pk)
            serializer = StoreDetailSerializer(
                store, many=False, context={"request": request}
            )
            return Response(serializer.data)
        except Store.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        store = Store.objects.get(pk=pk)
        store.name = request.data["name"]
        store.description = request.data["description"]

        customer = Customer.objects.get(user=request.auth.user)
        store.owner = customer

        store.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
