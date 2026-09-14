from rest_framework import generics
from .models import Orden, Cliente, Tecnico, DetalleOrden
from .serializers import (
    OrdenSerializer,
    ClienteSerializer,
    ClienteDetailSerializer,
    TecnicoSerializer,
    DetalleOrdenSerializer
)


# =====================================================================
# Vistas Basadas en Clases (Concrete Generic Views) para CRUD
# =====================================================================

class OrdenListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todas las órdenes con clientes, técnicos y detalles anidados.
    POST: Crea una orden nueva, permitiendo asignar cliente, técnico y detalles.
    """
    queryset = Orden.objects.all().select_related('cliente', 'tecnico').prefetch_related('detalles')
    serializer_class = OrdenSerializer


class OrdenDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Detalle de una orden específica con sus relaciones anidadas.
    PUT/PATCH: Actualización completa o parcial de la orden y sus detalles.
    DELETE: Eliminación de la orden.
    """
    queryset = Orden.objects.all().select_related('cliente', 'tecnico').prefetch_related('detalles')
    serializer_class = OrdenSerializer


class ClienteListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todos los clientes registrados.
    POST: Crea un nuevo cliente.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Detalle de un cliente incluyendo sus órdenes asociadas.
    PUT/PATCH: Actualización del cliente.
    DELETE: Eliminación del cliente.
    """
    queryset = Cliente.objects.all().prefetch_related('ordenes')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClienteDetailSerializer
        return ClienteSerializer


class TecnicoListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista de técnicos.
    POST: Crear un nuevo técnico.
    """
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer


class TecnicoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Detalle del técnico.
    PUT/PATCH: Actualización de datos del técnico.
    DELETE: Eliminación del técnico.
    """
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer


class DetalleOrdenListCreateView(generics.ListCreateAPIView):
    """
    GET: Lista todos los ítems/detalles de órdenes.
    POST: Crear un ítem/detalle de orden directamente.
    """
    queryset = DetalleOrden.objects.all().select_related('orden')
    serializer_class = DetalleOrdenSerializer


class DetalleOrdenDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Obtiene un detalle puntual.
    PUT/PATCH: Modifica un detalle puntual.
    DELETE: Elimina un detalle puntual.
    """
    queryset = DetalleOrden.objects.all().select_related('orden')
    serializer_class = DetalleOrdenSerializer