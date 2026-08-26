from rest_framework import serializers

from .models import Orden

class OrdenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orden
        fields = [
            "id",
            "numeroOrden",
            "nombre",
            "direccion",
            "altura",
            "tarea",
            "timestamp",
        ]

        read_only_fields = ["id", "timestamp"],