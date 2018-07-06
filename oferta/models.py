"""
Modelos del modulo de Ofertas del SIP. Por los momentos solamente
contiene la entidad Oferta, pues es la necesaria para el modulo.

Este archivo tambien implementa las senales de django, que permite
escuchar a eventos de interaccion con la bd y asi facilitar la integridad
y correctitud de datos.
"""

import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

from asignaturas.models import Asignatura
from coordinacion.models import Coordinacion


def anio_oferta_valido(anio_oferta):
    """Verifica que no se anada una oferta con un ano menor al ano actual
    """
    anio_hoy = datetime.datetime.now().year

    if anio_oferta < anio_hoy:
        raise ValidationError('El año de la oferta no puede ser menor al %d' % anio_hoy)

def trimestre_valido(trim):
    """
    Funcion que retorna True ssi el trimestre es valido
    """
    return trim in [0, 1, 2]

class Oferta(models.Model):
    """Modelo de la Base de Datos para una oferta.
    Contiene trimestre, anio, coordinacion y asignatura. Cada entrada en la base de datos
    de Oferta tiene que tener una combinacion unica de trimestre, anio y coordinacion.
    
    Se anaden choices de trimestre para el formulario de seleccion de este en la oferta
    lo cual permite guardar estas opciones como enteros en la base de datos pero obtener 
    la representacion textual de los valores 0, 1 y 2.
    """
    TRIMESTRE_ENEMAR = 0
    TRIMESTRE_ABRJUL = 1
    TRIMESTRE_SEPDIC = 2
    OFERTA_TRIMESTRE_CHOICES = (
        (TRIMESTRE_ENEMAR, 'Enero - Marzo'),
        (TRIMESTRE_ABRJUL, 'Abril - Julio'),
        (TRIMESTRE_SEPDIC, 'Septiembre - Diciembre')
    )

    trimestre = models.PositiveIntegerField(choices=OFERTA_TRIMESTRE_CHOICES,
                                            verbose_name="Trimestre")
    anio = models.PositiveIntegerField(verbose_name="Año")
    coordinacion = models.ForeignKey(Coordinacion, verbose_name='Coordinacion',
                                    related_name='ofertas', on_delete=models.CASCADE)

    # Se agrega un nuevo atributo que tiene las asignaturas que estan dentro de una oferta
    asignatura = models.ManyToManyField(Asignatura, verbose_name='Asignatura', related_name='ofertas')
    class Meta:
        unique_together = ('trimestre', 'anio', 'coordinacion')

    # Se agrega la funcion get_absolute_url para usar el createView
    def get_absolute_url(self):
        return reverse('oferta:dashboard')

@receiver(pre_save, sender=Oferta)
def valida_modelo(sender, **kwargs):
    """
    Funcion que se llama antes de guardar un objeto en la base de datos
    Funciona como los triggers de postgresql.
    """
    oferta = kwargs['instance']
    if not trimestre_valido(oferta.trimestre):
        raise ValidationError('El trimestre de la oferta debe estar entre 0 y 2')
