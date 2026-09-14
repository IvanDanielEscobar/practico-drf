from rest_framework import serializers
from .models import Orden, Cliente, Tecnico, DetalleOrden


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'email']


class TecnicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tecnico
        fields = ['id', 'nombre', 'categoria', 'activo']


class DetalleOrdenSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = DetalleOrden
        fields = ['id', 'orden', 'descripcion', 'cantidad', 'precio_unitario', 'subtotal']
        read_only_fields = ['id', 'subtotal']
        extra_kwargs = {
            'orden': {'required': False}
        }


class OrdenSerializer(serializers.ModelSerializer):
    # Serializers anidados para lectura
    cliente = ClienteSerializer(read_only=True)
    tecnico = TecnicoSerializer(read_only=True)
    detalles = DetalleOrdenSerializer(many=True, required=False)

    # Campos para escritura (asignación por ID)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Cliente.objects.all(),
        source='cliente',
        write_only=True
    )
    tecnico_id = serializers.PrimaryKeyRelatedField(
        queryset=Tecnico.objects.all(),
        source='tecnico',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Orden
        fields = [
            'id',
            'numeroOrden',
            'cliente',
            'cliente_id',
            'tecnico',
            'tecnico_id',
            'direccion',
            'altura',
            'tarea',
            'descripcion',
            'estado',
            'detalles',
            'timestamp',
            'updateTimestamp',
        ]
        read_only_fields = ['id', 'timestamp', 'updateTimestamp']

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles', [])
        orden = Orden.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleOrden.objects.create(orden=orden, **detalle_data)
        return orden

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if detalles_data is not None:
            instance.detalles.all().delete()
            for detalle_data in detalles_data:
                DetalleOrden.objects.create(orden=instance, **detalle_data)
        return instance


class ClienteDetailSerializer(serializers.ModelSerializer):
    """Serializer para ver el detalle de un cliente junto a sus órdenes anidadas."""
    ordenes = OrdenSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'telefono', 'email', 'ordenes']
