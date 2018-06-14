from django import forms
from django.forms import inlineformset_factory

from .models import Oferta 

class OfertaForm(forms.ModelForm):

    class Meta:
        model = Oferta 
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        trimestre = cleaned_data.get('trimestre')
        anio = cleaned_data.get('anio')
        coordinacion = cleaned_data.get('coordinacion')


