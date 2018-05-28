from django.contrib import admin

from .models import Asignatura, Horario, ProgramaAsignatura
# Register your models here.

admin.site.register(Asignatura)
admin.site.register(Horario)
admin.site.register(ProgramaAsignatura)