# create_groups.py
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

def create_groups():
    admin_group, created = Group.objects.get_or_create(name='Administrador')
    warehouse_group, created = Group.objects.get_or_create(name='Bodeguero')
    accountant_group, created = Group.objects.get_or_create(name='Contador')
    sales_group, created = Group.objects.get_or_create(name='Vendedor')

    # Asignar permisos a los grupos (opcional, depende de tu aplicación)
    # permission = Permission.objects.get(codename='some_permission')
    # admin_group.permissions.add(permission)

if __name__ == "__main__":
    create_groups()
