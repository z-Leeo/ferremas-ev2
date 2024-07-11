from django.db import models 
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class Marca(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=225)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    description = models.TextField()
    price = models.IntegerField()
    stock = models.PositiveIntegerField(default=0)  # Nuevo campo de stock
    image = models.ImageField(upload_to="Products", null=True)

    def __str__(self):
        return self.name
    
class CarritoItem(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def total(self):
        return self.producto.price * self.cantidad

    
class Contacto (models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    numero = models.IntegerField()
    asunto = models.CharField(max_length=50)
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre
    
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Agregar campos adicionales si es necesario
    
    class Meta:
        # Opcionalmente, puedes añadir configuraciones adicionales aquí
        pass

    # Agregar related_name para evitar conflictos de acceso inverso
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # Cambia a un nombre que prefieras
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Cambia a un nombre que prefieras
        related_query_name='user'
    )