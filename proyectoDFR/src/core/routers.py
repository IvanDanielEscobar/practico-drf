from django.urls import include, path
import ordenes.views as views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'ordenes', views.OrdenViewset, basename='orden')
router.register(r'clientes', views.ClienteListCreateViewset, basename='cliente')
router.register(r'tecnicos', views.TecnicoListCreateViewset, basename='tecnico')
router.register(r'detalles', views.DetalleOrdenListCreateViewset, basename='detalle')
