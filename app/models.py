from django.db import models 
import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission


class Marca(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=225)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    description = models.TextField()
    price = models.IntegerField()
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

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
        ('administrador', 'Administrador'),
        ('vendedor', 'Vendedor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Cambia esto para evitar el conflicto
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Cambia esto para evitar el conflicto
        blank=True,
    )