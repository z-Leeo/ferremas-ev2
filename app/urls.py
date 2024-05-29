from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import home,CheckOut,PaymentSuccessful,paymentFailed,ProductView,login,registro, currencyApi, salir,carrito,pedido

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('registro/', views.registro, name="registro"),
    path('productos/', views.ProductView, name='productos'),
    path('currencyApi/', views.currencyApi, name="currencyApi"),
    path('checkout/', views.CheckOut, name='checkout'),
    path('payment-success/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/', views.paymentFailed, name='payment-failed'),
    path('salir/', views.salir, name='salir'),
    path('carrito/', views.carrito, name="carrito"),
    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('pedido/', views.pedido, name='pedido'),
]