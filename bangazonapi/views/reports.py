from django.shortcuts import render
from bangazonapi.models import Order
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

class Reports(ViewSet):
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
        