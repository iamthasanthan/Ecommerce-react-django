from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import BankDetails, BuyerDetail, CustomUser, SellerDetail, SellerImages, ShippingAddress
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email']
    fieldsets = (
        (
            (('User'), {
                'fields': ('username', 'password', 'email', 'phone_number', 'user_type')
            }),
            # (('Payment'), {
            #     'fields': ()
            # }),
            (('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }),
        ))


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ShippingAddress)
admin.site.register(BankDetails)
admin.site.register(BuyerDetail)
admin.site.register(SellerDetail)
admin.site.register(SellerImages)


admin.site.site_header = "CT PORTAL"
admin.site.site_title = "CT PORTAL"
admin.site.index_title = "CT PORTAL"
