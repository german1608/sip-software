"""
Archivo que tiene los modelos correspondientes a este modulo.
"""

from django.db import models


class Coordinacion(models.Model):
    """
    Entidad Coordinacion que se almacena en la base de datos
    """
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
        return self.nombre
