from django import forms
from django.forms import inlineformset_factory
from .models import Asignatura, Horario, ProgramaAsignatura

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = '__all__'

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = ProgramaAsignatura
        fields = '__all__'

ProgramaFormset = inlineformset_factory(Asignatura, ProgramaAsignatura, form=ProgramaForm, min_num=1, extra=0, can_delete=True)
HorarioFormset = inlineformset_factory(Asignatura, Horario, form=HorarioForm, min_num=1, extra=0, can_delete=True)
