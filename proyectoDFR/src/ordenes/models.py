from django.db import models


class Orden(models.Model):
    numeroOrden = models.IntegerField()
    nombre = models.CharField(max_length=150),
    direccion = models.Charfield(max_lenght=150),
    altura = models.IntegerField(),
    tarea = models.CharField(max_length=250),
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nombre

    