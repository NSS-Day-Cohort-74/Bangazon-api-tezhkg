from django.shortcuts import render
from django.contrib.auth.models import User
from bangazonapi.models import Favorite, Store
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

class Report(ViewSet):
    
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
