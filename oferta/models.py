import datetime
from django.db import models
from django.core.exceptions import ValidationError
from coordinacion.models import Coordinacion
from django.urls import reverse

# Create your models here.
def anio_oferta_valido(anio_oferta):
    anio_hoy = datetime.datetime.now().year

    if anio_oferta < anio_hoy:
        raise ValidationError('El año de la oferta no puede ser menor al %d' % anio_hoy)

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

    # Se agrega la funcion get_absolute_url para usar el createView
    def get_absolute_url(self):
        return reverse('oferta:dashboard')
