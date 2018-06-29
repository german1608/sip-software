"""
Formularios de modulo de ofertas. Facilitan la interaccion
del usuario con la base de datos.
"""

from django import forms
from django.forms import modelformset_factory

from asignaturas.models import Asignatura

from .models import Oferta


class OfertaForm(forms.ModelForm):
    """
    Clase que permite crear formularios para crear o actualizar Ofertas
    academicas.
    """

    class Meta:
        model = Oferta 
        fields = ['trimestre', 'anio', 'coordinacion']

AsignaturaFormset = modelformset_factory(Asignatura, fields=('id',), extra=1)
