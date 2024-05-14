from django.shortcuts import render
from .models import Product
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

def home(request):
    return render(request, 'app/home.html')

def login(request):
    return render(request, 'app/login.html')

def registro(request):
    return render(request, 'app/registro.html')


def currencyApi(request):
    return render(request, 'app/currencyApi.html')


def ProductView(request):

    get_products = Product.objects.all()

    return render(request, 'app/productos.html', {'products': get_products})

def CheckOut(request, product_id):

    product = Product.objects.get(id=product_id)

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': product.price,
        'item_name': product.name,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success', kwargs = {'product_id': product.id})}",
        'cancel_url': f"http://{host}{reverse('payment-failed', kwargs = {'product_id': product.id})}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    context = {
        'product': product,
        'paypal': paypal_payment
    }

    return render(request, 'app/checkout.html', context)

def PaymentSuccessful(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'app/payment-success.html', {'product': product})

def paymentFailed(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request, 'app/payment-failed.html', {'product': product})
