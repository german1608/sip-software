from django.db import models

# Create your models here.
class Coordinacion(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, primary_key=True)
