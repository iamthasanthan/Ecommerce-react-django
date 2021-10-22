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


@api_view(['GET'])
def all_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    if SellerDetail.objects.filter(user=request.user).exists():
        if request.method == "GET":
            products = Product.objects.filter(seller=request.user)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            serializer = ProductUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    if SellerDetail.objects.filter(user=request.user).exists():
        try:
            product = Product.objects.get(id=pk)

        except Product.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if request.method == "GET":
            serializer = ProductSerializer(product)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "PUT":
            serializer = ProductUpdateSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_100_CONTINUE)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif request.method == "DELETE":
            product.delete()
            return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def all_offers_product(request, pk):
    try:
        offers = ProductOffer.objects.filter(
            product__id=pk, offer_available=True)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    serializer = ProductOfferSerializer(offers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_offer(request, pk, offer_id):
    if SellerDetail.objects.filter(user=request.user).exists():
        try:
            product = Product.objects.get(id=pk)
            offer = ProductOffer.objects.get(id=offer_id, product=product)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if SellerDetail.objects.filter(user=request.user):
            if request.method == "GET":
                offers = ProductOffer.objects.filter(product=product)
                serializer = ProductOfferSerializer(offers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif request.method == "POST":
                serializer = ProductOfferUpdateSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            elif request.method == "PUT":
                serializer = ProductOfferUpdateSerializer(
                    offer, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            elif request.method == "DELETE":
                offer.delete()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_review(request, pk):
    try:
        product = Product.objects.get(id=pk)
        product_reviews = ProductReviews.objects.filter(product=product)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = ProductReviewsSerializer(product_reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ProductReviewsUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_review(request, pk, review_id):
    try:
        product = Product.objects.get(id=pk)
        product_review = ProductReviews.objects.get(
            product=product, id=review_id)
    except ProductReviews.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = ProductReviewsSerializer(product_review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if product_review.user == request.user:
            serializer = ProductReviewsUpdateSerializer(
                product_review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "DELETE":
        if product_review.user == request.user:
            product_review.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_product_images(request, pk):
    try:
        product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        images = ProductImages.objects.filter(product=product)
        serializer = ProductImagesSerializer(images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        if SellerDetail.objects.filter(user=request.user).exists():
            serializer = ProductImagesUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_product_image(request, pk, image_id):
    try:
        product = Product.objects.get(id=pk)
        image = ProductImages.objects.get(product=product, id=image_id)
    except ProductImages.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = ProductImagesSerializer(image)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        if product.seller == request.user:
            serializer = ProductImagesUpdateSerializer(
                image, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == "DELETE":
        if product.seller == request.user:
            image.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
