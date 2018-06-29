"""
Integracion del modulo de profesores al admin site de django.
"""
from django.contrib import admin

from .models import Profesor
# Register your models here.

admin.site.register(Profesor)