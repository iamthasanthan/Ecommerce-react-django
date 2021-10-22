from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from .serializers import *
from users.models import *
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
# Create your views here.
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def payment_info(request):
    try:
        payment = PaymentInfo.objects.filter(user=request.user).first()
    except PaymentInfo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PaymentInfoSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = PaymentInfoSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        serializer = PaymentInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        payment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def purchase_product(request):
    try:
        purchases = Purchase.objects.filter(buyer=request.user)
    except Purchase.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def cancel_purchase(request, payment_id):
    try:
        purchase = Purchase.objects.get(id=payment_id)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serailizer = PurchaseSerializer(purchase)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        purchase.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def add_deliveries(request):
    try:
        delivers = Delivery.objects.filter(deliverer=request.user)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = DeliverySerializer(delivers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = DeliverySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_delivery(request, delivery_id):
    try:
        delivery = Delivery.objects.get(id=delivery_id, deliverer=request.user)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = DeliverySerializer(delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
