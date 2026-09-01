from django.shortcuts import render, get_object_or_404
from django.decorators import api_view
from django.response import Response
from rest_framework import status
from .models import Orden, Cliente, Tecnico
from .serializers import OrdenSerializer,ClienteSerializer,TecnicoSerializer

# CRUD  

@api_view(['GET', 'POST'])
def crear_lista_orden(request):
    """
        GET: Lista todas las ordenes
        POST: Crea una nueva orden vinculada a un cliente existente
    """

    if request.method == 'GET':
        ordenes = Orden.objects.all().select_related('cliente', 'tecnico')
        serializer = OrdenSerializer(ordenes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = OrdenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def ordenDetail(request, pk):
    """
    el get trae el detalle de una orden 
    put actualiza una orden completa
    delete elimina la orden
    """
    orden = get_object_or_404(Orden, pk=pk)

    if request.method == 'GET':
        serializer = OrdenSerializer(orden)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = OrdenSerializer(orden, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTPS_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        orden.delete()
        return Response({'mensaje': f'Orden #{orden.numeroOrden} eliminada'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def cliente_lista_crear(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)