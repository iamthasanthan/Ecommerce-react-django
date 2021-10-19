from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from store.models import Product

# Create your models here.


class PaymentInfo(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{} paid {} for {} posted by {}".format(self.user.username, self.price, self.product.name, self.product.seller.username)
