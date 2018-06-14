from django import forms
from django.forms import inlineformset_factory

from .models import Oferta 

class OfertaForm(forms.ModelForm):

    class Meta:
        model = Oferta 
        fields = '__all__'
