from django.shortcuts import render
from .models import *
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.contrib.auth import  logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import viewsets
from .serializers import ProductSerializer, MarcaSerializer




class MarcaViewset(viewsets.ModelViewSet):
    queryset = Marca.objects.all()
    serializer_class = MarcaSerializer


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        productos = Product.objects.all()

        name = self.request.GET.get('name')

        if name:
            productos = productos.filter(name__contains=name)

        return productos



def home (request):
    if request.method == 'POST':
        nombreContc = request.POST.get('nombre')
        correoContc = request.POST.get('email')
        numeroContc = request.POST.get('numero')
        asuntoContc = request.POST.get('asunto')
        mensajeContc = request.POST.get('mensaje')

        contactoHome = Contacto.objects.create(nombre = nombreContc
                                                ,email = correoContc
                                                ,numero = numeroContc
                                                ,asunto = asuntoContc
                                                ,mensaje = mensajeContc)
        contactoHome.save()
        return redirect('home')
    return render (request , 'app/home.html')

from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.views import View

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.user_type == 'bodeguero':
                return redirect('bodeguero')
            elif user.user_type == 'contador':
                return redirect('contador')
            elif user.user_type == 'administrador':
                return redirect('administrador')
            elif user.user_type == 'vendedor':
                return redirect('vendedor')
        return render(request, 'registration/login.html', {'form': form})

@login_required
def bodeguero_view(request):
    return render(request, 'app/bodeguero.html')

@login_required
def contador_view(request):
    return render(request, 'app/contador.html')

@login_required
def administrador_view(request):
    return render(request, 'app/administrador.html')

@login_required
def vendedor_view(request):
    return render(request, 'app/vendedor.html')

def registro(request):
    return render(request, 'registration/registro.html')

@login_required
def pedido(request):
    return render(request, 'app/pedido.html')

@login_required
def currencyApi(request):
    return render(request, 'app/currencyApi.html')

import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
import requests
import logging
logger = logging.getLogger(__name__)

def convert_currency(request):
    if request.method == 'GET' and 'currency' in request.GET:
        target_currency = request.GET['currency']
        
        # URL de la API de conversión de moneda
        api_url = f'https://v6.exchangerate-api.com/v6/07c7436812f210f455d48d84/latest/'
        
        try:
            response = requests.get(api_url)
            data = response.json()
            
            if response.status_code == 200 and 'conversion_rates' in data:
                rates = data['conversion_rates']
                
                if target_currency in rates:
                    rate = rates[target_currency]
                    return JsonResponse({'success': True, 'rate': rate})
                else:
                    return JsonResponse({'success': False, 'error': f'No se encontró la tasa para {target_currency}'})
            else:
                logger.error(f'Error al obtener las tasas de cambio - Status code: {response.status_code}, Data: {data}')
                return JsonResponse({'success': False, 'error': 'Error al obtener las tasas de cambio'})
        
        except requests.RequestException as e:
            logger.error(f'Error en la solicitud HTTP: {str(e)}')
            return JsonResponse({'success': False, 'error': f'Error en la solicitud HTTP: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido o parámetros faltantes'})



@login_required
def ProductView(request):
   # Ordena los productos por el campo 'nombre' (puedes cambiar 'nombre' por el campo que desees)
    get_products = Product.objects.all()  
    page = request.GET.get('page', 1)
    try:
        paginator = Paginator(get_products, 9)
        get_products = paginator.page(page)
    except:
        raise Http404
    

    data = {
        'entity': get_products,
        'paginator': paginator,
        
    }

    return render(request, 'app/productos.html', data)

@login_required
def CheckOut(request):
    carrito_items = CarritoItem.objects.all()
    host = request.get_host()

    if not carrito_items:
        return HttpResponseBadRequest('El carrito está vacío')

    total_amount = sum(item.total for item in carrito_items)

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_amount,
        'item_name': 'Compra en línea',
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success')}",
        'cancel_url': f"http://{host}{reverse('payment-failed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'carrito_items': carrito_items,
        'paypal': paypal_payment,
        'total_carrito': total_amount,
    }

    return render(request, 'app/checkout.html', context)

@login_required
def PaymentSuccessful(request):
    carrito_items = CarritoItem.objects.all()
    for item in carrito_items:
        producto = item.producto
        producto.stock -= item.cantidad
        producto.save()
    
    CarritoItem.objects.all().delete()  # Limpiar el carrito después del pago exitoso
    return render(request, 'app/payment-success.html')

@login_required
def paymentFailed(request):
    return render(request, 'app/payment-failed.html')


def salir(request):
    logout(request)
    return render(request,'app/home.html')


def user_belongs_to_admin_group(user):
    return user.groups.filter(name='admin').exists()

from django.http import HttpResponseBadRequest

@login_required
def carrito(request):
    if request.method == 'POST':
        form_product_id = request.POST.get('producto_id')
        if form_product_id:
            try:
                producto = Product.objects.get(pk=form_product_id)
            except Product.DoesNotExist:
                return HttpResponseBadRequest('Producto no encontrado')
            cantidad = int(request.POST.get('cantidad', 1))
            carrito_item, created = CarritoItem.objects.get_or_create(producto=producto)
            carrito_item.cantidad = cantidad  # Aquí se actualiza la cantidad directamente
            carrito_item.save()
            return redirect('carrito')  # Redirigir a la página del carrito sin ningún argumento
        else:
            return HttpResponseBadRequest('ID de producto no proporcionado')
    else:
        carrito = CarritoItem.objects.all()
        total_carrito = sum(item.total for item in carrito)
        productos_en_carrito = [{'producto': item.producto, 'cantidad': item.cantidad, 'total': item.total} for item in carrito]
        data = {
            'productos_en_carrito': productos_en_carrito,
            'total_carrito': total_carrito,
        }
        return render(request, 'app/carrito.html', data)

def eliminar_producto(request, producto_id):
    carrito_item = get_object_or_404(CarritoItem, producto__id=producto_id)
    carrito_item.delete()
    return redirect('carrito')

from django.db.models import Q


@login_required
def buscar(request):
    termino = request.GET.get('buscar', '')

    # Filtra los productos según el término de búsqueda
    productos = Product.objects.filter(
        Q(name__icontains=termino) | 
        Q(marca__name__icontains=termino)
    )


    data = {
        'entity': productos,
        'termino': termino
    }

    return render(request, 'app/productos.html', data)



