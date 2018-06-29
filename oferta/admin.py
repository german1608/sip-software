"""
Integracion del modulo de ofertas en el admin site de django.
"""

from django.contrib import admin

from .models import Oferta

# Register your models here.

admin.site.register(Oferta)
