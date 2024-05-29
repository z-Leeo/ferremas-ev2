from django.shortcuts import render
from .models import *
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.contrib.auth import  logout
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

def login(request):
    return render(request, 'registration/login.html')

def registro(request):
    return render(request, 'registration/registro.html')

@login_required
def pedido(request):
    return render(request, 'app/pedido.html')

@login_required
def currencyApi(request):
    return render(request, 'app/currencyApi.html')

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
        'paginator': paginator
    }

    return render(request, 'app/productos.html', data)

@login_required
def CheckOut(request):
    carrito_items = CarritoItem.objects.all()
    host = request.get_host()

    carrito = CarritoItem.objects.all()
    total_carrito = sum(item.total for item in carrito)

    
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
        'total_carrito': total_carrito,
    }

    return render(request, 'app/checkout.html', context)

def PaymentSuccessful(request):
    CarritoItem.objects.all().delete()  # Limpiar el carrito después del pago exitoso
    return render(request, 'app/payment-success.html')

def paymentFailed(request):
    return render(request, 'app/payment-failed.html')


def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_trabajador = 'trabajador' in request.POST
        is_ingtec = 'ingtec' in request.POST
        is_supervisor = 'supervisor' in request.POST

        if not any([is_trabajador, is_ingtec, is_supervisor]):
            # Puedes manejar el error de alguna manera, por ejemplo, mostrar un mensaje de error.
            return render(request, 'registration/registro.html', {'error_message': 'Selecciona al menos un grupo de usuario.'})

        # Crear el usuario
        user = User.objects.create_user(username=username, password=password)

        # Asignar el grupo correspondiente al usuario
        if is_trabajador:
            trabajador_group, _ = Group.objects.get_or_create(name='trabajador')
            user.groups.add(trabajador_group)
        if is_ingtec:
            ingtec_group, _ = Group.objects.get_or_create(name='ingtec')
            user.groups.add(ingtec_group)
        if is_supervisor:
            supervisor_group, _ = Group.objects.get_or_create(name='supervisor')
            user.groups.add(supervisor_group)

        # Redirigir a la página de inicio de sesión
        return redirect('login')  # Reemplaza 'nombre_de_la_url_de_login' con el nombre de la URL de tu vista de inicio de sesión.

    return render(request, 'registration/registro.html')

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
            if not created:
                carrito_item.cantidad += cantidad
            else:
                carrito_item.cantidad = cantidad
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



