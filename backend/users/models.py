from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

USer_TYPE_CHOICES = (
    ('admin', 'Admin'),
    ('manager', 'Manager'),
    ('seller', 'Seller'),
    ('buyer', 'Buyer'),
    ('viewer', 'Viewer'),
)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=120, unique=True, blank=True, null=True)

    password = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone_number = models.CharField(max_length=120, blank=True, null=True)
    user_type = models.CharField(
        max_length=120, choices=USer_TYPE_CHOICES, default='viewer')

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class ShippingAddress(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    current = models.BooleanField(default=False)

    def __str__(self):
        return "{} entered {}".format(self.user.username, self.address)


class BankDetails(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=100)
    bank_account_number = models.CharField(max_length=100)
    bank_user_name = models.CharField(
        max_length=120, blank=True, null=True)

    def __str__(self):
        return "{} entered {}".format(self.user.username, self.bank_name)


class BuyerDetail(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{} address added for {}".format(self.shipping_address, self.user.username)


class SellerImages(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='seller/business_images/')
    show = models.BooleanField(default=True)

    def __str__(self) -> str:
        return "{} image {}".format(self.user.username, self.id)


class SellerDetail(models.Model):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    business_description = models.TextField()
    business_address = models.CharField(max_length=100)
    business_phone_number = models.CharField(max_length=100)
    business_email = models.EmailField(max_length=100)
    business_website = models.CharField(max_length=100)
    business_logo = models.ImageField(upload_to='seller/business_logo/')
    business_cover_photo = models.ImageField(
        upload_to='seller/business_cover_photo/')

    business_type = models.CharField(max_length=100)
    business_location = models.CharField(max_length=100)

    def __str__(self) -> str:
        return "{} added details".format(self.user.username)
