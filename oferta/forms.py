from django import forms
from django.forms import modelformset_factory
from asignaturas.models import Asignatura
from .models import Oferta

class OfertaForm(forms.ModelForm):

    class Meta:
        model = Oferta 
        fields = ['trimestre', 'anio', 'coordinacion']

AsignaturaFormset = modelformset_factory(Asignatura, fields=('id',), extra=1)
