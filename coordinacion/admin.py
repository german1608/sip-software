"""
Archivo que genera el admin site del proyecto.
Nada mas registramos la Coordinacion al admin.
"""

from django.contrib import admin
from .models import Coordinacion
# Register your models here.

admin.site.register(Coordinacion)
