from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cliente, Tecnico, Orden, DetalleOrden


class OrdenesAPITests(APITestCase):
    def setUp(self):
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

    def test_crear_cliente(self):
        url = reverse('cliente-list-create')
        data = {
            "nombre": "Ana Martinez",
            "telefono": "3517654321",
            "email": "ana.martinez@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.count(), 2)

    def test_crear_orden_con_detalles_anidados(self):
        url = reverse('orden-list-create')
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
