from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import CustomUser
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
                'fields': ('username', 'password', 'email', 'business_name', 'business_address')
            }),
            (('Payment'), {
                'fields': ('bank_name', 'bank_account_number')
            }),
            (('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }),
        ))


admin.site.register(CustomUser, CustomUserAdmin)
