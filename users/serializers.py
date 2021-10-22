from rest_framework.authtoken.views import Token
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import serializers
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class BankDetailsSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = BankDetails
        fields = '__all__'


class BankDetailsUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankDetails

        fields = '__all__'


class SellerImagesSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SellerImages
        fields = '__all__'


class SellerImagesUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerImages
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ShippingAddress
        fields = '__all__'


class ShippingAddressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress

        fields = '__all__'


class SellerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SellerDetail
        fields = '__all__'


class SellerDetailUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerDetail
        fields = '__all__'


class BuyerDetailUpdateSerializer(serializers.ModelSerializer):
    # user = UserSerializer()

    class Meta:
        model = BuyerDetail
        fields = ['user', 'approved']


class BuyerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = BuyerDetail
        fields = '__all__'
