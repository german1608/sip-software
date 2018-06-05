from django import forms
from django.forms import inlineformset_factory
from .models import Asignatura, Horario, ProgramaAsignatura
from django.core.exceptions import ValidationError
import datetime

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = '__all__'
    def clean_creditos(self):
        creditos = self.cleaned_data['creditos']
        if creditos <= 0 :
            raise ValidationError('Los créditos deben ser mayor a cero')
        return creditos

    def clean_fecha_de_ejecucion(self):
        fecha_de_ejecucion = self.cleaned_data['fecha_de_ejecucion']
        if fecha_de_ejecucion > datetime.date.today() :
            raise ValidationError('La fecha de ejecución debe ser hoy o antes de hoy')
        return fecha_de_ejecucion

class HorarioForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_final = cleaned_data.get("hora_final")
        if hora_inicio > hora_final or hora_inicio == hora_final:
            raise forms.ValidationError("Error. La hora de inicio debe ser menor que la hora final")

    class Meta:
        model = Horario
        fields = '__all__'

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = ProgramaAsignatura
        fields = '__all__'

ProgramaFormset = inlineformset_factory(Asignatura, ProgramaAsignatura, form=ProgramaForm, min_num=1, extra=0, can_delete=True)
HorarioFormset = inlineformset_factory(Asignatura, Horario, form=HorarioForm, min_num=1, extra=0, can_delete=True)
