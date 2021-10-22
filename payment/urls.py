from django.urls import path

from .views import *

urlpatterns = [
    path('', payment_info, name='payment-info'),
    path('purchase/', purchase_product, name="purchase-product"),
    path('purchase/<int:payment_id>/', cancel_purchase, name="cancel-purchase"),
    path('deliveries/', add_deliveries, name="add-delivery"),
    path('deliveries/<int:delivery_id>/',
         update_delivery, name="update-delivery")
]
