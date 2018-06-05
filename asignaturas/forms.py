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
    class Meta:
        model = Horario
        fields = '__all__'

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = ProgramaAsignatura
        fields = '__all__'

    def clean_url(self):
        url = self.cleaned_data['url']
        protocolo = url.split(":")[0]
        if not (protocolo == 'https' or protocolo == 'http') :
            raise ValidationError('El protocolo del programa no es válido')
        return url

ProgramaFormset = inlineformset_factory(Asignatura, ProgramaAsignatura, form=ProgramaForm, min_num=1, extra=0, can_delete=True)
HorarioFormset = inlineformset_factory(Asignatura, Horario, form=HorarioForm, min_num=1, extra=0, can_delete=True)
