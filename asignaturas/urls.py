from django.contrib import admin
from django.urls import path
from asignaturas.views import Busqueda

app_name = 'asignaturas'
urlpatterns = [
    path('', Busqueda.as_view(), name='busqueda'),
]
