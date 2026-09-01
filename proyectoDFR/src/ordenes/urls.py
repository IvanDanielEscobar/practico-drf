from django.urls import path
from . import views

urlpatterns = [
    path('ordenes/', views.crear_lista_orden, name='crear_lista_orden'),
    path('ordenes/<int:pk>'),
    path('clientes/', views.ordenDetail, name='ordenDetail'),
]



