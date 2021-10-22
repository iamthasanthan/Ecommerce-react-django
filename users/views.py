from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from .serializers import *

from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def userprofileview(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def user_create(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def user_detail_edit(request):

    try:
        user = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user, many=False)
        print(serializer)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def add_bank_details(request):
    user = request.user

    if request.method == 'POST':
        if BankDetails.objects.filter(user=request.user).exists():
            Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            serializer = BankDetailsUpdateSerializer(data=request.data)

            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        if BankDetails.objects.filter(user=request.user).exists():

            bank_detail = BankDetails.objects.get(user=request.user)
            serializer = BankDetailsUpdateSerializer(
                bank_detail, data=request.data, many=False)

            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == 'GET':
        if BankDetails.objects.filter(user=request.user).exists():
            print("TEst")
            bank_details = BankDetails.objects.get(user=user)
            serializer = BankDetailsSerializer(bank_details)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def add_address(request):
    if request.method == 'POST':
        serializer = ShippingAddressUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if ShippingAddress.objects.filter(user=request.user).exists():
            address = ShippingAddress.objects.filter(user=request.user)
            serializer = ShippingAddressSerializer(address, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def update_shipping_address(request, pk):
    if request.method == 'PUT':
        try:
            address = ShippingAddress.objects.get(id=pk)
            serializer = ShippingAddressUpdateSerializer(
                address, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ShippingAddress.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'GET':
        try:
            address = ShippingAddress.objects.get(id=pk)
            serializer = ShippingAddressSerializer(address)
            return Response(serializer.data)
        except ShippingAddress.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'DELETE':
        try:
            address = ShippingAddress.objects.get(id=pk)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ShippingAddress.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def buyerdetail(request):
    if request.method == "GET":
        if BuyerDetail.objects.filter(user=request.user).exists():
            buyer_detail = BuyerDetail.objects.get(user=request.user)
            serializer = BuyerDetailSerializer(buyer_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        if BuyerDetail.objects.filter(user=request.user).exists():
            Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = BuyerDetailUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        if BuyerDetail.objects.filter(user=request.user).exists():
            buyer_detail = BuyerDetail.objects.get(user=request.user)
            serializer = BuyerDetailUpdateSerializer(
                buyer_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "DELETE":
        if BuyerDetail.objects.filter(user=request.user).exists():
            bankdetail = BuyerDetail.objects.get(user=request.user)

            bankdetail.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def sellerdetail(request):
    if request.method == "GET":
        if SellerDetail.objects.filter(user=request.user).exists():
            seller_detail = SellerDetail.objects.get(user=request.user)
            serializer = SellerDetailSerializer(seller_detail)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        if SellerDetail.objects.filter(user=request.user).exists():
            Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = SellerDetailUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        if SellerDetail.objects.filter(user=request.user).exists():
            seller_detail = SellerDetail.objects.get(user=request.user)
            serializer = SellerDetailUpdateSerializer(
                seller_detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == "DELETE":
        if SellerDetail.objects.filter(user=request.user).exists():
            seller_detail = SellerDetail.objects.get(user=request.user)

            seller_detail.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def sellerimages(request):
    if request.method == "POST":
        serializer = SellerImagesUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        if SellerImages.objects.filter(user=request.user).exists():
            sellerimages_details = SellerImages.objects.filter(
                user=request.user)
            serializer = SellerImagesSerializer(
                sellerimages_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication])
def updatesellerimages(request, pk):
    try:
        seller_image = SellerImages.objects.get(id=pk)
    except SellerImages.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PUT":
        serializer = SellerImagesUpdateSerializer(
            seller_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":

        serializer = SellerImagesSerializer(
            seller_image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        seller_image.delete()
        return Response(status=status.HTTP_200_OK)
