from .models import *
from rest_framework import serializers
from users.serializers import *
from users.models import *
from store.serializers import *
from store.models import *


class PaymentInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = PaymentInfo
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True, many=True)
    payment_info = PaymentInfoSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    purchases = PurchaseSerializer(read_only=True, many=True)

    deliverer = UserSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'
