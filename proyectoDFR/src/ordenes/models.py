from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    telefono = models.CharField(max_length=30)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

class Tecnico(models.Model):
    class CategoriasTecnicos(models.TextChoices):
        mantenimiento = 'MANTENIMIENTO', 'Mantenimiento'
        instalaciones = 'INSTALACIONES', 'Instalaciones'

    nombre = models.CharField(max_length=120)
    categoria =  models.CharField( max_length=20,choices=CategoriasTecnicos.choices, default=CategoriasTecnicos.mantenimiento)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

class Orden(models.Model):
    class EstadoOrden(models.TextChoices):
        PENDIENTE = 'PENDIENTE', 'Pendiente'
        EN_PROCESO = 'EN_PROCESO', 'En Proceso'
        COMPLETADA = 'COMPLETADA', 'Completada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    numeroOrden = models.PositiveIntegerField(unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ordenes')
    tecnico = models.ForeignKey(Tecnico, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordenes_asignadas')
    direccion = models.CharField(max_length=150)
    altura = models.PositiveIntegerField()
    tarea = models.CharField(max_length=250)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=EstadoOrden.choices,
        default=EstadoOrden.PENDIENTE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updateTimestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Orden #{self.numeroOrden} - {self.cliente.nombre}"