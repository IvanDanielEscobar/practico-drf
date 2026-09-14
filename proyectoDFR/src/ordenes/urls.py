from django.urls import path
from . import views

urlpatterns = [
    # Órdenes
    path('ordenes/', views.OrdenListCreateView.as_view(), name='orden-list-create'),
    path('ordenes/<int:pk>/', views.OrdenDetailView.as_view(), name='orden-detail'),

    # Clientes
    path('clientes/', views.ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<int:pk>/', views.ClienteDetailView.as_view(), name='cliente-detail'),

    # Técnicos
    path('tecnicos/', views.TecnicoListCreateView.as_view(), name='tecnico-list-create'),
    path('tecnicos/<int:pk>/', views.TecnicoDetailView.as_view(), name='tecnico-detail'),

    # Detalles individuales de órdenes
    path('detalles/', views.DetalleOrdenListCreateView.as_view(), name='detalle-list-create'),
    path('detalles/<int:pk>/', views.DetalleOrdenDetailView.as_view(), name='detalle-detail'),
]
