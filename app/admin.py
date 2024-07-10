from django.contrib import admin
from .models import Product, Marca, Contacto, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Product)
admin.site.register(Marca)
admin.site.register(Contacto)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext, gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('User Type'), {'fields': ('user_type',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_type')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)