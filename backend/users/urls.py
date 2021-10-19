from django.urls import path
from .views import *

urlpatterns = [
    path('', userprofileview, name='user-profile'),
    path('edit/', user_detail_edit, name='edit-profile'),
    path('register/', user_create, name='register'),
    path('bank_detail/', add_bank_details, name="bank-detail"),
]
