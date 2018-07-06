"""
Modelo del modulo de profesores del SIP. Contiene una sola entidad

- Coordinación.

"""

from django.db import models


class Coordinacion(models.Model):
    """
    Entidad Coordinacion que se almacena en la base de datos y
    contiene los datos necesario que contiene esta.
    -nombre
    -código
    """
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, primary_key=True)

    def __str__(self):
	    """ 
	    Se agrega la funcion para imprimir el objeto Profesor de una manera 
	    amigable para el usuario.
	    """
	    return self.nombre
