from django.contrib import admin
from django.urls import path
from .views import *

app_name = 'oferta'

urlpatterns = [
    path('', index, name='dashboard')
]