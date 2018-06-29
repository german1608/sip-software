"""
Configuracion del admin del modulo de asignaturas.
Anade las entidades Asignatura, Horario y ProgramaAsignatura al admin.
"""

from django.contrib import admin

from .models import Asignatura, Horario, ProgramaAsignatura

# Register your models here.

admin.site.register(Asignatura)
admin.site.register(Horario)
admin.site.register(ProgramaAsignatura)
