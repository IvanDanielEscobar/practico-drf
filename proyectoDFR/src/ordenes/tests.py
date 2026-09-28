from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cliente, Tecnico, Orden, DetalleOrden


class OrdenesAPITests(APITestCase):
    def setUp(self):
        # 1. Crear usuario de prueba y autenticar mediante JWT (SimpleJWT)
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )
        token_url = reverse('token_obtain_pair')
        token_response = self.client.post(
            token_url,
            {"username": "testuser", "password": "testpassword123"},
            format='json'
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.access_token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # 2. Datos iniciales
        self.cliente = Cliente.objects.create(
            nombre="Juan Perez",
            telefono="3511234567",
            email="juan.perez@example.com"
        )
        self.tecnico = Tecnico.objects.create(
            nombre="Carlos Gomez",
            categoria=Tecnico.CategoriasTecnicos.mantenimiento,
            activo=True
        )

    # -------------------------------------------------------------
    # Tests de Seguridad y Autenticación JWT (Práctico 3)
    # -------------------------------------------------------------
    def test_obtener_token_jwt(self):
        """Verifica que el endpoint /api/token/ devuelva tokens access y refresh."""
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            "username": "testuser",
            "password": "testpassword123"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_seguridad_escritura_sin_token_rechazada(self):
        """Verifica que intentar crear recursos sin token devuelva 401 Unauthorized."""
        # Desautenticar temporalmente al cliente
        self.client.credentials()

        url = reverse('cliente-list')
        data = {
            "nombre": "Anonimo",
            "telefono": "000000000",
            "email": "anonimo@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tecnico_readonly_model_viewset(self):
        """
        Verifica que TecnicoViewSet (ReadOnlyModelViewSet) permita lectura (GET 200)
        y bloquee la creación con 405 Method Not Allowed.
        """
        # Lectura permitida
        url_list = reverse('tecnico-list')
        response_get = self.client.get(url_list)
        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

        # Escritura bloqueada
        data = {"nombre": "Nuevo Tecnico", "categoria": "INSTALACIONES", "activo": True}
        response_post = self.client.post(url_list, data, format='json')
        self.assertEqual(response_post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # -------------------------------------------------------------
    # Tests de CRUD y Serializers Anidados (con Router y ModelViewSet)
    # -------------------------------------------------------------
    def test_crear_cliente(self):
        url = reverse('cliente-list')
        data = {
            "nombre": "Ana Martinez",
            "telefono": "3517654321",
            "email": "ana.martinez@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_crear_orden_con_detalles_anidados(self):
        url = reverse('orden-list')
        data = {
            "numeroOrden": 1001,
            "cliente_id": self.cliente.id,
            "tecnico_id": self.tecnico.id,
            "direccion": "Av. Colon",
            "altura": 1234,
            "tarea": "Instalacion de router y cableado",
            "descripcion": "Instalacion en planta alta",
            "estado": "PENDIENTE",
            "detalles": [
                {
                    "descripcion": "Router Mikrotik",
                    "cantidad": 1,
                    "precio_unitario": "75000.00"
                },
                {
                    "descripcion": "Metro cable UTP Cat6",
                    "cantidad": 30,
                    "precio_unitario": "1200.50"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        orden = Orden.objects.get(numeroOrden=1001)
        self.assertEqual(orden.detalles.count(), 2)
        self.assertEqual(orden.cliente, self.cliente)
        self.assertEqual(orden.tecnico, self.tecnico)

        # Verificar respuesta con serializers anidados
        self.assertEqual(response.data['cliente']['nombre'], "Juan Perez")
        self.assertEqual(response.data['tecnico']['nombre'], "Carlos Gomez")
        self.assertEqual(len(response.data['detalles']), 2)
        self.assertEqual(float(response.data['detalles'][0]['subtotal']), 75000.00)
        self.assertEqual(float(response.data['detalles'][1]['subtotal']), 36015.00)

    def test_obtener_detalle_orden_anidada(self):
        orden = Orden.objects.create(
            numeroOrden=1002,
            cliente=self.cliente,
            tecnico=self.tecnico,
            direccion="San Martin",
            altura=555,
            tarea="Mantenimiento preventivo",
            estado="PENDIENTE"
        )
        DetalleOrden.objects.create(
            orden=orden,
            descripcion="Filtro de aire",
            cantidad=2,
            precio_unitario="5000.00"
        )

        url = reverse('orden-detail', kwargs={'pk': orden.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['numeroOrden'], 1002)
        self.assertEqual(response.data['cliente']['id'], self.cliente.id)
        self.assertEqual(len(response.data['detalles']), 1)
        self.assertEqual(response.data['detalles'][0]['descripcion'], "Filtro de aire")
        self.assertEqual(float(response.data['detalles'][0]['subtotal']), 10000.00)

    def test_actualizar_orden_y_detalles(self):
        orden = Orden.objects.create(
            numeroOrden=1003,
            cliente=self.cliente,
            tecnico=self.tecnico,
            direccion="Rivadavia",
            altura=100,
            tarea="Reparacion",
            estado="PENDIENTE"
        )
        url = reverse('orden-detail', kwargs={'pk': orden.pk})
        data = {
            "numeroOrden": 1003,
            "cliente_id": self.cliente.id,
            "tecnico_id": self.tecnico.id,
            "direccion": "Rivadavia",
            "altura": 100,
            "tarea": "Reparacion",
            "estado": "EN_PROCESO",
            "detalles": [
                {
                    "descripcion": "Mano de obra",
                    "cantidad": 1,
                    "precio_unitario": "25000.00"
                }
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estado'], "EN_PROCESO")
        self.assertEqual(orden.detalles.count(), 1)

    def test_eliminar_orden(self):
        orden = Orden.objects.create(
            numeroOrden=1004,
            cliente=self.cliente,
            direccion="Belgrano",
            altura=200,
            tarea="Prueba eliminacion",
            estado="PENDIENTE"
        )
        url = reverse('orden-detail', kwargs={'pk': orden.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Orden.objects.filter(pk=orden.pk).exists())
