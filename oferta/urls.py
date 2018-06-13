from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'oferta'

urlpatterns = [
    path('', index, name='dashboard'),
    path('anadir/', OfertaAgregar.as_view(), name='anadir-oferta'),
    path('json', oferta_json, name='oferta-json'),
]