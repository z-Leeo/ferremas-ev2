# middleware.py
from django.shortcuts import redirect

class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and not request.user.is_superuser:
            if request.user.groups.filter(name='Administrador').exists():
                return redirect('admin_dashboard')
            elif request.user.groups.filter(name='Bodeguero').exists():
                return redirect('warehouse_dashboard')
            elif request.user.groups.filter(name='Contador').exists():
                return redirect('accountant_dashboard')
            elif request.user.groups.filter(name='Vendedor').exists():
                return redirect('sales_dashboard')
        return response
