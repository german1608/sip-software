"""
Formularios del modulo de asignaturas. Contiene 3 formularios:
- AsignaturaForm
- HorarioForm
- ProgramaForm

Los 3 se deben usar en conjunto, pues todos corresponden a la creacion
o actualizacion de una asignatura.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Asignatura, Horario, ProgramaAsignatura
from django.core.exceptions import ValidationError
import datetime

class AsignaturaForm(forms.ModelForm):
    """
    Formulario que renderiza y administra todos los campos del formulario de 
    asignaturas ya sea para creación o edición. Los campos a mostrar en el 
    formulario son determinados por los campos existentes en el Modelo 'Asignatura'.

    Este formulario contiene dos validadores importantes. Por una parte 
    clean_creditos, que al ser introducidos un numero de creditos negativo, 
    el formulario se convierte en inválido y retorna un mensaje de error y 
    por otra parte, clean_fecha_de_ejecucion, que asegura que la fecha de
    ejecucion de una asignatura no sea una fecha en el futuro.
    """
    class Meta:
        model = Asignatura
        fields = '__all__'

    # Validador de creditos. Deben ser positivos.    
    def clean_creditos(self):
        creditos = self.cleaned_data['creditos']
        if creditos <= 0 :
            raise ValidationError('Los créditos deben ser mayor a cero')
        return creditos

    # Validador de fecha de ejecucion. Una asignatura no puede
    # tener una fecha de ejecución en el futuro.
    def clean_fecha_de_ejecucion(self):
        fecha_de_ejecucion = self.cleaned_data['fecha_de_ejecucion']
        if fecha_de_ejecucion > datetime.date.today() :
            raise ValidationError('La fecha de ejecución debe ser hoy o antes de hoy')
        return fecha_de_ejecucion

class HorarioForm(forms.ModelForm):
    """
    Formulario que renderiza y administra todos los campos del formulario de 
    horarios que es parte de la creación o edición de una asignatura. 
    Los campos a mostrar en el formulario son determinados por los campos 
    existentes en el Modelo 'Horario'.

    Este formulario valida que la hora de inicio no sea mayor a la hora final
    mediante el metodo clean.
    """
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
    """
    Formulario que renderiza y administra todos los campos del formulario de 
    programas que es parte de la creación o edición de una asignatura. 
    Los campos a mostrar en el formulario son determinados por los campos 
    existentes en el Modelo 'ProgramaAsignatura'.
    """    
    class Meta:
        model = ProgramaAsignatura
        fields = '__all__'

ProgramaFormset = inlineformset_factory(Asignatura, ProgramaAsignatura, form=ProgramaForm, min_num=1, extra=0, can_delete=True)
HorarioFormset = inlineformset_factory(Asignatura, Horario, form=HorarioForm, min_num=1, extra=0, can_delete=True)
