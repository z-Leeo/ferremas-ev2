from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import home,CheckOut,PaymentSuccessful,paymentFailed,ProductView,login,registro, currencyApi, salir,carrito,pedido,ProductViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('get_products',ProductViewset)

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
    path('api/', include(router.urls)),
    path('bodeguero/', views.bodeguero_view, name='bodeguero_view'),
    path('contador/', views.contador_view, name='contador_view'),
    path('administrador/', views.administrador_view, name='administrador_view'),
    path('vendedor/', views.vendedor_view, name='vendedor_view'),
]