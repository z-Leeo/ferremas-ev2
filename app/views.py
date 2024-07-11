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

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import Group

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.groups.filter(name='bodeguero').exists():
                    return redirect('warehouse_dashboard')
                elif user.groups.filter(name='contador').exists():
                    return redirect('accountant_dashboard')
                elif user.groups.filter(name='administrador').exists():
                    return redirect('admin_dashboard')
                elif user.groups.filter(name='vendedor').exists():
                    return redirect('sales_dashboard')
                else:
                    return redirect('home')  # Redirige a la home si no pertenece a ningún grupo
        return render(request, 'registration/login.html', {'form': form})


from django.shortcuts import render
from django.views import View

class AdminDashboardView(View):
    def get(self, request):
        return render(request, 'app/admin_dashboard.html')

class WarehouseDashboardView(View):
    def get(self, request):
        return render(request, 'app/warehouse_dashboard.html')

class AccountantDashboardView(View):
    def get(self, request):
        return render(request, 'app/accountant_dashboard.html')

class SalesDashboardView(View):
    def get(self, request):
        return render(request, 'app/sales_dashboard.html')
# app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required





from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            username = formulario.cleaned_data.get('username')
            raw_password = formulario.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Te has registrado correctamente.')
            return redirect('home')
        else:
            data['form'] = formulario
    return render(request, 'registration/registro.html', data)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CarritoItem, Product


@login_required
def pedido(request):
    if request.method == 'POST':
        # Procesar el formulario de pedido aquí
        nombre = request.POST.get('nombre')
        domicilio = request.POST.get('domicilio')
        celular = request.POST.get('celular')
        email = request.POST.get('email')
        metodo_pedido = request.POST.get('metodo_pedido')
        metodo_pago = request.POST.get('metodo_pago')

        # Obtener productos en el carrito de alguna manera alternativa
        carrito_items = CarritoItem.objects.all()  # Cambia esto a la lógica que usas en la vista del carrito

        if not carrito_items:
            return HttpResponseBadRequest('El carrito está vacío')

        total_amount = sum(item.total for item in carrito_items)

        # Almacenar la información del pedido en la sesión para pasarla a la vista de checkout
        request.session['pedido_data'] = {
            'nombre': nombre,
            'domicilio': domicilio,
            'celular': celular,
            'email': email,
            'metodo_pedido': metodo_pedido,
            'metodo_pago': metodo_pago,
            'total_amount': total_amount,
        }

        return redirect('checkout')
    
    else:
        carrito_items = CarritoItem.objects.all()  # Cambia esto a la lógica que usas en la vista del carrito

        if not carrito_items:
            return HttpResponseBadRequest('El carrito está vacío')

        total_amount = sum(item.total for item in carrito_items)
        
        data = {
            'carrito_items': carrito_items,
            'total_carrito': total_amount,
        }
        return render(request, 'app/pedido.html', data)


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
    get_products = Product.objects.filter(stock__gt=0).order_by('name') 
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
    # Obtener todos los ítems en el carrito
    carrito_items = CarritoItem.objects.all()

    # Procesar cada ítem en el carrito
    for item in carrito_items:
        producto = item.producto
        producto.stock -= item.cantidad
        producto.save()

    # Calcular el total del carrito (si es necesario para tu lógica)
    total_carrito = sum(item.total for item in carrito_items)

    # Limpiar el carrito después del pago exitoso
    CarritoItem.objects.all().delete()

    # Recuperar información del pedido desde la sesión
    pedido_data = request.session.get('pedido_data', {})

    context = {
        'carrito_items': carrito_items,  # Pasar los ítems del carrito a la plantilla
        'total_carrito': total_carrito,
        'nombre': pedido_data.get('nombre'),
        'domicilio': pedido_data.get('domicilio'),
        'celular': pedido_data.get('celular'),
        'email': pedido_data.get('email'),
        'metodo_pedido': pedido_data.get('metodo_pedido'),
        'metodo_pago': pedido_data.get('metodo_pago'),  # Pasar el total del carrito si es necesario
        # Ajustar según tu lógica de moneda
    }

    return render(request, 'app/payment-success.html', context)

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



