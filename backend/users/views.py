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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def add_bank_details(request):
    user = request.user

    if request.method == 'POST':
        if BankDetails.objects.filter(user=request.user).exists():
            Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            serializer = BankDetailsSerializer(data=request.data)

            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        if BankDetails.objects.filter(user=request.user).exists():
            serializer = BankDetailsSerializer(
                user=user, data=request.data, many=False)
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


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication, TokenAuthentication, ])
def add_address(request):
    if request.method == 'POST':
        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        if ShippingAddress.objects.filter(user=request.user).exists():
            address = ShippingAddress.objects.filter(user=request.user)
            serializer = ShippingAddressSerializer(address)
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
            serializer = ShippingAddressSerializer(address, data=request.data)
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
