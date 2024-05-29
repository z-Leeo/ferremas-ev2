from django.contrib import admin
from .models import Product, Marca, Contacto

# Register your models here.
admin.site.register(Product)
admin.site.register(Marca)
admin.site.register(Contacto)