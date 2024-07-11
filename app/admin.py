from django.contrib import admin
from .models import Product, Marca, Contacto
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.
admin.site.register(Product)
admin.site.register(Marca)
admin.site.register(Contacto)

# Unregister the original User admin
admin.site.unregister(User)

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'groups'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        # Assign role to user
        super().save_model(request, obj, form, change)
        if 'groups' in form.cleaned_data:
            groups = form.cleaned_data['groups']
            obj.groups.set(groups)
            obj.save()

# Re-register UserAdmin
admin.site.register(User, UserAdmin)