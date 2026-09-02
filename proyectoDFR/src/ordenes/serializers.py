from rest_framework import serializers

from .models import Orden, Cliente, Tecnico


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = '__all__'

class OrdenSerializer(serializers.ModelSerializer):
    #estos son para que en el get se vea el nombre del cliente y el tecnico ademas del id
    clienteNombre = serializers.ReadOnlyField(source='cliente.nombre')
    tecnicoNombre = serializers.ReadOnlyField(source='tecnico.nombre')
    class Meta:
        model = Orden
        fields = [
            "id",
            "numeroOrden",
            "cliente",
            "clienteNombre",
            "tecnico",
            "tecnicoNombre",
            "direccion",
            "altura",
            "tarea",
            "descripcion",
            "timestamp",
        ]

        read_only_fields = ["id", "timestamp"]