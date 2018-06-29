"""
Formularios de modulo de ofertas. Facilitan la interaccion
del usuario con la base de datos.
"""

from django import forms

from .models import Oferta

class OfertaForm(forms.ModelForm):
    """
    Clase que permite crear formularios para crear o actualizar Ofertas
    academicas.
    """

    class Meta:
        model = Oferta 
        fields = ['trimestre', 'anio', 'coordinacion']
