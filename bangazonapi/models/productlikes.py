from  django.db import models



class ProductLikes(models.Model):



#     product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="ratings")
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])