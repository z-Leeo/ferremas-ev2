from .models import Product, Marca
from rest_framework import serializers


class MarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marca
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    name_marca = serializers.CharField(read_only=True, source="marca.name")
    marca = MarcaSerializer(read_only=True)
    marca_id = serializers.PrimaryKeyRelatedField(queryset=Marca.objects.all(), source="marca")
    name = serializers.CharField(required=True, min_length=3)

    def validate_name(self, value):
        existe = Product.objects.filter(name__iexact=value).exists()

        if existe:
            raise  serializers.ValidationError("Este producto ya existe")
        return value

    class Meta:
        model = Product
        fields = '__all__'
