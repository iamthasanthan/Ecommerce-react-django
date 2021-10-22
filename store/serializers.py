from rest_framework import serializers
from .models import *
from users.serializers import *


class ProductSerializer(serializers.ModelSerializer):
    seller = UserSerializer

    class Meta:
        model = Product
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductOfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductOffer
        fields = '__all__'


class ProductOfferUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOffer
        fields = '__all__'


class ProductReviewsSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductReviews
        fields = '__all__'


class ProductReviewsUpdateSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductReviews
        fields = '__all__'


class ProductImagesSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductImagesUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = '__all__'
