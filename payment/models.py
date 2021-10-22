from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from store.models import Product

# Create your models here.
PAID_STATUS = (
    ('Paid', 'Paid'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
)
DELIVERY_STATUS = (
    ('Delivered', 'Delivered'),
    ('Pending', 'Pending'),
    ('Cancelled', 'Cancelled'),
)


class PaymentInfo(models.Model):
    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=50)
    exp_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    current = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username


class Purchase(models.Model):
    buyer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller')
    product = models.ManyToManyField(Product)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=PAID_STATUS, max_length=10, default='Pending')
    payment_info = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{} paid {} for {}".format(self.buyer.username, self.amount, self.seller.username)


class Delivery(models.Model):
    buyer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=DELIVERY_STATUS,
                              max_length=10, default='Pending')
    purchases = models.ManyToManyField(Purchase)
    added_date = models.DateTimeField(auto_now_add=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    deliverer = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deliverer')

    def __str__(self) -> str:
        return "{} is delivering {} purchases".format(self.buyer.username, self.purchases.count())
