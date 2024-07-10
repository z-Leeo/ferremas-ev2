# app/tests.py
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Marca, CustomUser

class ProductModelTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(name="Test Marca")
        self.producto = Product.objects.create(
            name="Test Producto",
            marca=self.marca,
            description="Descripción de prueba",
            price=100,
            stock=10,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

    def test_product_creation(self):
        self.assertIsInstance(self.producto, Product)
        self.assertEqual(self.producto.__str__(), self.producto.name)
        self.assertEqual(self.producto.marca.name, "Test Marca")

class ProductViewTest(TestCase):
    def setUp(self):
        self.marca = Marca.objects.create(name="Test Marca")
        self.producto = Product.objects.create(
            name="Test Producto",
            marca=self.marca,
            description="Descripción de prueba",
            price=100,
            stock=10,
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )
        self.user = CustomUser.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_product_list_view(self):
        response = self.client.get(reverse('productos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.producto.name)
        self.assertTemplateUsed(response, 'app/productos.html')

    def test_search_product_by_name(self):
        response = self.client.get(reverse('buscar') + '?buscar=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Producto')
        self.assertTemplateUsed(response, 'app/productos.html')

    def test_search_product_by_marca(self):
        response = self.client.get(reverse('buscar') + '?buscar=Test Marca')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Producto')
        self.assertTemplateUsed(response, 'app/productos.html')



from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Marca, CarritoItem

class CarritoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.marca = Marca.objects.create(name="Test Marca")
        self.producto = Product.objects.create(
            name="Test Producto",
            marca=self.marca,
            description="Descripción de prueba",
            price=100,
            stock=10,
            image="test_image.jpg"
        )
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_agregar_producto_al_carrito(self):
        response = self.client.post(reverse('carrito'), {'producto_id': self.producto.id, 'cantidad': 1})
        self.assertEqual(response.status_code, 302)
        carrito_item = CarritoItem.objects.get(producto=self.producto)
        self.assertEqual(carrito_item.cantidad, 1)

    def test_eliminar_producto_del_carrito(self):
        CarritoItem.objects.create(producto=self.producto, cantidad=1)
        response = self.client.post(reverse('eliminar_producto', args=[self.producto.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CarritoItem.objects.filter(producto=self.producto).exists())

    def test_calculo_total_carrito(self):
        CarritoItem.objects.create(producto=self.producto, cantidad=2)
        carrito_items = CarritoItem.objects.all()
        total_carrito = sum(item.total for item in carrito_items)
        self.assertEqual(total_carrito, 200)

    def test_actualizar_cantidad_en_carrito(self):
        CarritoItem.objects.create(producto=self.producto, cantidad=1)
        response = self.client.post(reverse('carrito'), {'producto_id': self.producto.id, 'cantidad': 3})
        self.assertEqual(response.status_code, 302)
        carrito_item = CarritoItem.objects.get(producto=self.producto)
        self.assertEqual(carrito_item.cantidad, 3)
        self.assertEqual(carrito_item.total, 300)



from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Marca, CarritoItem

class CheckoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.marca = Marca.objects.create(name="Test Marca")
        self.producto = Product.objects.create(
            name="Test Producto",
            marca=self.marca,
            description="Descripción de prueba",
            price=100,
            stock=10,
            image="test_image.jpg"
        )
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        CarritoItem.objects.create(producto=self.producto, cantidad=1)

    def test_checkout_con_carrito_lleno(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Producto')
        self.assertContains(response, '100')

    def test_checkout_con_carrito_vacio(self):
        CarritoItem.objects.all().delete()
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 400)

    def test_checkout_reduce_stock(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.stock, 8)  # Originalmente 10 - 2 comprados

    def test_checkout_vaciar_carrito_despues_pago(self):
        response = self.client.get(reverse('payment-success'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CarritoItem.objects.exists())


from django.test import TestCase, Client
from django.urls import reverse
from app.models import Contacto

class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_contact_form_submission(self):
        response = self.client.post(reverse('home'), {
            'nombre': 'John Doe',
            'email': 'johndoe@example.com',
            'numero': '123456789',
            'asunto': 'Test Subject',
            'mensaje': 'This is a test message.'
        })
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after successful form submission
        self.assertTrue(Contacto.objects.filter(email='johndoe@example.com').exists())

