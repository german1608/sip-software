from django import forms

from .models import Oferta

class OfertaForm(forms.ModelForm):

    class Meta:
        model = Oferta 
        fields = ['trimestre', 'anio', 'coordinacion']

class OfertaDetailsForm(forms.ModelForm):
    """
    Formulario para la vista de detalles
    """
    class Meta:
        model = Oferta
        fields = '__all__'
