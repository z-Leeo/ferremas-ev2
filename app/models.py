from django.db import models

# Create your models here.
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
        return self.product.price * self.cantidad