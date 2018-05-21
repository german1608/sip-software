# Generated by Django 2.0.5 on 2018-05-21 15:08

from django.db import migrations, models
import profesores.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('primer_nombre', models.CharField(max_length=100, verbose_name='Primer Nombre')),
                ('segundo_nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Segundo Nombre')),
                ('primer_appelido', models.CharField(max_length=100, verbose_name='Primer Apellido')),
                ('segundo_apellido', models.CharField(blank=True, max_length=100, null=True, verbose_name='Segundo Apellido')),
                ('cedula', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Cédula')),
                ('carnet', models.CharField(max_length=10, unique=True, verbose_name='Carné')),
                ('fecha_nacimiento', models.DateField(validators=[profesores.models.fecha_nacimiento_valida], verbose_name='Fecha de Nacimiento')),
            ],
        ),
    ]
