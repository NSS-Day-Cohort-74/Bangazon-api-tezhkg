from django.db import models
from .customer import Customer

class Store(models.Model):

# Store Name
    name = models.CharField(max_length=55)
# Store Description
    description = models.CharField(max_length=155)
# Customer ID (Creator/Owner)
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="store") 

