from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.crear_lista_orden, name='crear_lista_orden'),
    path('ordenes/<int:pk>', views.ordenDetail, name='ordenDetail'),
    path('clientes/', views.cliente_lista_crear, name='cliente_lista_crear'),
]



