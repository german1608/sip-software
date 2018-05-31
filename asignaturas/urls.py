from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'asignaturas'
urlpatterns = [
    path('', Index.as_view(), name='dashboard'),
    path('tabla', AsignaturasAsJson.as_view(), name='all-json'),
    path('detalles/<int:pk>', AsignaturaDetallesView.as_view(), name='detalles'),
    path('eliminar/', EliminarAsignaturaView.as_view(), name='eliminar-asignatura'),
    path('editar/', EditarAsignaturaView.as_view(), name='editar-asignatura'),
    path('anadir/', AnadirAsignaturaView.as_view(), name='anadir-asignatura')
]
