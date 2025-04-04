from  django.db import models
from .customer import Customer

class ProductLike(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="product_likes")

