# Generated by Django 2.0.5 on 2018-06-11 01:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asignaturas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignatura',
            name='codasig',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(code='codigo_invalido', message='Formato de código incorrecto. Ej: CO3121', regex='^[A-Z]{2}[0-9]{4}$')], verbose_name='Código de Asignatura'),
        ),
        migrations.AlterField(
            model_name='programaasignatura',
            name='url',
            field=models.CharField(max_length=500, validators=[django.core.validators.URLValidator()], verbose_name='Código de Programa'),
        ),
    ]