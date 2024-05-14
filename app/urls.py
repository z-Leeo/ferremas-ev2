from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import home,CheckOut,PaymentSuccessful,paymentFailed,ProductView,login,registro, currencyApi

urlpatterns = [
    path('', home , name="home"),
    path('login/' ,login,  name="login"),
    path('registro/',registro, name= "registro"),
    path('productos/', views.ProductView, name='productos'),
    path('currencyApi/', currencyApi, name="currencyApi"),
    path('checkout/<int:product_id>/', views.CheckOut, name='checkout'),
    path('payment-success/<int:product_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:product_id>/', views.paymentFailed, name='payment-failed'),
   
]