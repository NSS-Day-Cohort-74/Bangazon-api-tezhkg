from django.shortcuts import render
from django.contrib.auth.models import User
from bangazonapi.models import Order, Product, Favorite, Store
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class Reports(ViewSet):
    #In this approach, I decided to add the use TokenAuthentication and IsAuthenticated from the DRF, 
    # and then add authentication_classes and permission_classes to the ViewSet.
    #This should require all report endpoints to require a valid auth token.
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @action(methods=["get"],detail=False)
    def favoritesellers(self,request):
        #Get the customer_id to find the user information and create the report title variable
        customer_id = self.request.query_params.get("customer")
        customer = User.objects.get(customer=customer_id)
        report_title = f"{customer.first_name} {customer.last_name}'s Favorite Sellers"

        #Get all the sellers favored by the customer
        favorite_sellers = Favorite.objects.filter(customer_id = customer_id)
        
        #Iterate through the sellers and return only the store names
        store_list = []
        for seller in favorite_sellers:
            store = Store.objects.get(pk=seller.store_id)
            store_list += {store.name}
    
        context = {
            "stores":store_list,
            "report_title": report_title
        }

        return render(request, "reports/favoritesellers.html", context)
    @action(methods=["get"], detail=False)
    def orders(self, request):
        status = self.request.query_params.get("status")

        if status == "complete":
            orders = Order.objects.filter(payment_type__isnull=False)

            for order in orders:
                order.total = 0
                for line_item in order.lineitems.all():
                    order.total += line_item.product.price

            context = {"orders": orders, "report_title": "Completed Orders"}

            return render(request, "reports/completed_orders.html", context)
        
        if status == "incomplete":
            # get all the orders where the payment_type has not been added
            orders = Order.objects.filter(payment_type__isnull=True)

            # Iterate through the orders, summing the cost of each item and adding it to a total_cost field
            for order in orders:
                order.total_cost = 0
                for line_item in order.lineitems.all():
                    order.total_cost += line_item.product.price

            # Create context to pass to the Template
            context = {"orders": orders, "report_title": "Incomplete Orders Report"}

            return render(request, "reports/incomplete_orders.html", context)
        
    @action(methods=["get"], detail=False) 
    def inexpensiveproducts(self, request):
      
        products = Product.objects.filter(price__lte=999)

      
        context = {
            "products": products,
            "report_title": "Products Under $999"
        }

        return render(request, "reports/products.html", context)

    @action(methods=["get"], detail=False) 
    def expensiveproducts(self, request):
        
            products = Product.objects.filter(price__gt=999)

        
            context = {
                "products": products,
                "report_title": "Products Over $999"
            }

            return render(request, "reports/products.html", context)
