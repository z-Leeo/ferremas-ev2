from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import home,CheckOut,PaymentSuccessful,paymentFailed,ProductView,LoginView,registro, currencyApi, salir,carrito,pedido,ProductViewset,MarcaViewset, buscar,AdminDashboardView, WarehouseDashboardView, AccountantDashboardView, SalesDashboardView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('get_products',ProductViewset)
router.register('marca', MarcaViewset)

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', LoginView.as_view(), name='login'),
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
    path('buscar/', buscar, name='buscar'), # type: ignore
    path('api/', include(router.urls)),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('warehouse_dashboard/', WarehouseDashboardView.as_view(), name='warehouse_dashboard'),
    path('accountant_dashboard/', AccountantDashboardView.as_view(), name='accountant_dashboard'),
    path('sales_dashboard/', SalesDashboardView.as_view(), name='sales_dashboard'),
    # Otras URLs de la aplicación
]