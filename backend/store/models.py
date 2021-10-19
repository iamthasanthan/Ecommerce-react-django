from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    seller = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    product_image = models.ImageField(upload_to='product/image/', blank=True)
    product_banner_image = models.ImageField(
        upload_to='product/banner/', blank=True)

    def __str__(self) -> str:
        return "{} posted in {}".format(self.name, self.seller.business_name)


class ProductOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_available = models.BooleanField(default=False)
    offer_price = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    offer_start_date = models.DateTimeField(blank=True, null=True)
    offer_end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return "{} offer created price {}".format(self.product.name, self.offer_price)


class ProductReviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "{} review posted by {}".format(self.product.name, self.user.username)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')

    def __str__(self) -> str:
        return "{} image {}".format(self.product.name, self.id)
