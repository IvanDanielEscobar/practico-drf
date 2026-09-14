<<<<<<< HEAD
from rest_framework import generics
from .models import Orden, Cliente, Tecnico, DetalleOrden
from .serializers import (
    OrdenSerializer,
    ClienteSerializer,
    ClienteDetailSerializer,
    TecnicoSerializer,
    DetalleOrdenSerializer
)
=======
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Orden, Cliente, Tecnico
from .serializers import OrdenSerializer,ClienteSerializer,TecnicoSerializer
>>>>>>> 157d3084cfe88b5cb379661f2ca16a07360c4cd2


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
<<<<<<< HEAD
    queryset = Orden.objects.all().select_related('cliente', 'tecnico').prefetch_related('detalles')
    serializer_class = OrdenSerializer
=======
    orden = get_object_or_404(Orden, pk=pk)

    if request.method == 'GET':
        serializer = OrdenSerializer(orden)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = OrdenSerializer(orden, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        orden.delete()
        return Response({'mensaje': f'Orden #{orden.numeroOrden} eliminada'}, status=status.HTTP_204_NO_CONTENT)
>>>>>>> 157d3084cfe88b5cb379661f2ca16a07360c4cd2


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