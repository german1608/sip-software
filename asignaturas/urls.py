from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'asignaturas'
urlpatterns = [
    path('', index, name='index'),
    path('eliminar-asignatura/', EliminarAsignaturaView.as_view(), name='eliminar-asignatura')
]
