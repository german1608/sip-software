import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from coordinacion.models import Coordinacion
from django.urls import reverse

# Create your models here.
def anio_oferta_valido(anio_oferta):
    anio_hoy = datetime.datetime.now().year

    if anio_oferta < anio_hoy:
        raise ValidationError('El año de la oferta no puede ser menor al %d' % anio_hoy)

def trimestre_valido(trim):
    """
    Funcion que True ssi el trimestre es valido
    """
    return trim in [0, 1, 2]

class Oferta(models.Model):
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
    anio = models.PositiveIntegerField(verbose_name="Año",
                                       validators=[anio_oferta_valido])
    coordinacion = models.ForeignKey(Coordinacion, verbose_name='Coordinacion',
                                    related_name='ofertas', on_delete=models.CASCADE)

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
    anio_oferta_valido(oferta.anio)
