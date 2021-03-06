# Generated by Django 2.0.5 on 2018-06-11 01:13

import django.db.models.deletion
from django.db import migrations, models

import oferta.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coordinacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trimestre', models.PositiveIntegerField(choices=[(0, 'Enero - Marzo'), (1, 'Abril - Julio'), (2, 'Septiembre - Diciembre')], verbose_name='Trimestre de la oferta')),
                ('anio', models.PositiveIntegerField(validators=[oferta.models.anio_oferta_valido], verbose_name='Año de la oferta')),
                ('coordinacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ofertas', to='coordinacion.Coordinacion', verbose_name='Coordinacion')),
            ],
        ),
    ]
