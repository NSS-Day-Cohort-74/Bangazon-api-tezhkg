from django.shortcuts import render
from bangazonapi.models import Order
from bangazonapi.models import Product
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action


class Reports(ViewSet):
    @action(methods=["get"], detail=False)
    def orders(self, request):
        status = self.request.query_params.get("status")

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

        return render(request, "reports/inexpensive_products.html", context)