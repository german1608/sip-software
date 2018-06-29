"""
Modelo del modulo de profesores del SIP. Contiene una sola entidad

- Profesor
"""

from django.db import models
from django.core.exceptions import ValidationError
import datetime

def fecha_nacimiento_valida(fecha):
    hoy = datetime.date.today()
    if fecha > hoy:
        raise ValidationError('La fecha de nacimiento no puede ser despues de hoy')

class Profesor(models.Model):
    """
    Entidad Profesor. Contiene los datos necesarios para representar
    un profesor en la vida real.

    - primer nombre
    - segundo nombre
    - primer apellido
    - segundo apellido
    - cedula
    - carnet
    - fecha nacimiento
    """
    primer_nombre = models.CharField(max_length=100, verbose_name='Primer Nombre')
    segundo_nombre = models.CharField(max_length=100, null=True, blank=True,
        verbose_name='Segundo Nombre')
    primer_apellido = models.CharField(max_length=100, verbose_name='Primer Apellido')
    segundo_apellido = models.CharField(max_length=100, null=True, blank=True,
        verbose_name='Segundo Apellido')
    cedula = models.CharField(max_length=10, primary_key=True, verbose_name='Cédula')
    carnet = models.CharField(max_length=10, unique=True, verbose_name='Carné')
    fecha_nacimiento = models.DateField(validators=[fecha_nacimiento_valida],
        verbose_name='Fecha de Nacimiento')

    # Se agrega la funcion para imprimir el objeto Profesor de una manera 
    # user friendly 
    def __str__(self):
        return self.primer_nombre + " " + self.primer_apellido