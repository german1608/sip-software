from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'asignaturas'
urlpatterns = [
    path('', IndexView.as_view(), name="dashboard"),
    path('eliminar/', EliminarAsignaturaView.as_view(), name='eliminar-asignatura')
]
