from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'oferta'

urlpatterns = [
    path('', index, name='dashboard'),
    path('anadir/', OfertaAgregar.as_view(), name='anadir-oferta'),
    path('editar/<int:pk>/', OfertaEditar.as_view(), name="editar-oferta"),
    path('json', oferta_json, name='oferta-json'),
    path('eliminar/<pk>', EliminarOferta.as_view(), name='eliminar-oferta'),
    path('descargar/', DescargarOfertasView.as_view(), name='descargar'),
    path('detalle/<int:pk>', DetallesOferta.as_view(), name='detalles-oferta')
]
