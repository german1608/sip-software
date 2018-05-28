from django import forms
from django.forms import inlineformset_factory
from .models import Asignatura, Horario, ProgramaAsignatura

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = '__all__'

ProgramaFormset = inlineformset_factory(Asignatura, ProgramaAsignatura, fields='__all__', extra=1)
HorarioFormset = inlineformset_factory(Asignatura, Horario, fields='__all__', extra=1)
