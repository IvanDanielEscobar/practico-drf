from rest_framework import viewsets, permissions
from .models import Orden, Cliente, Tecnico, DetalleOrden
from .serializers import (
    OrdenSerializer,
    ClienteSerializer,
    ClienteDetailSerializer,
    TecnicoSerializer,
    DetalleOrdenSerializer
)


# =====================================================================
# ViewSets (ModelViewSet y ReadOnlyModelViewSet)
# =====================================================================

class OrdenViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de órdenes.
    - GET /api/ordenes/: Listado con datos anidados.
    - POST /api/ordenes/: Creación con detalles anidados.
    - GET /api/ordenes/{id}/: Detalle específico.
    - PUT / PATCH / DELETE /api/ordenes/{id}/: Modificación y borrado.
    Seguridad: Lectura abierta / Modificaciones solo para usuarios autenticados (JWT).
    """
    queryset = Orden.objects.all().select_related('cliente', 'tecnico').prefetch_related('detalles')
    serializer_class = OrdenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD completo de clientes.
    - Usa ClienteDetailSerializer en 'retrieve' para mostrar órdenes anidadas.
    - Usa ClienteSerializer en el resto de acciones.
    Seguridad: Lectura abierta / Modificaciones solo para usuarios autenticados (JWT).
    """
    queryset = Cliente.objects.all().prefetch_related('ordenes')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClienteDetailSerializer
        return ClienteSerializer


class TecnicoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ReadOnlyModelViewSet para técnicos.
    Solo permite operaciones de lectura:
    - GET /api/tecnicos/ (list)
    - GET /api/tecnicos/{id}/ (retrieve)
    Bloquea automáticamente POST, PUT, PATCH y DELETE.
    """
    queryset = Tecnico.objects.all()
    serializer_class = TecnicoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class DetalleOrdenViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones directas sobre ítems o detalles de órdenes.
    Seguridad: Lectura abierta / Modificaciones solo para usuarios autenticados (JWT).
    """
    queryset = DetalleOrden.objects.all().select_related('orden')
    serializer_class = DetalleOrdenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]