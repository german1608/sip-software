from django.db import models
from django.core.exceptions import ValidationError
import datetime

def fecha_nacimiento_valida(fecha):
    hoy = datetime.date.today()
    if fecha > hoy:
        raise ValidationError('La fecha de nacimiento no puede ser despues de hoy')

# Create your models here.
class Profesor(models.Model):
    primer_nombre = models.CharField(max_length=100, verbose_name='Primer Nombre')
    segundo_nombre = models.CharField(max_length=100, null=True, blank=True,
        verbose_name='Segundo Nombre')
    primer_appelido = models.CharField(max_length=100, verbose_name='Primer Apellido')
    segundo_apellido = models.CharField(max_length=100, null=True, blank=True,
        verbose_name='Segundo Apellido')
    cedula = models.CharField(max_length=10, primary_key=True, verbose_name='Cédula')
    carnet = models.CharField(max_length=10, unique=True, verbose_name='Carné')
    fecha_nacimiento = models.DateField(validators=[fecha_nacimiento_valida],
        verbose_name='Fecha de Nacimiento')
