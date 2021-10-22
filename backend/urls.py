
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('store/', include("store.urls")),
    path('payment/', include("payment.urls")),
]
