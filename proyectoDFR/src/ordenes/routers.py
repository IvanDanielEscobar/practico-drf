from rest_framework.routers import DefaultRouter
from .views import (
    OrdenViewSet,
    ClienteViewSet,
    TecnicoViewSet,
    DetalleOrdenViewSet,
)

router = DefaultRouter()
router.register(r'ordenes', OrdenViewSet, basename='orden')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'tecnicos', TecnicoViewSet, basename='tecnico')
router.register(r'detalles', DetalleOrdenViewSet, basename='detalle')
