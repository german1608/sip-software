# Generated by Django 2.0.5 on 2018-05-31 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asignaturas', '0006_auto_20180531_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programaasignatura',
            name='url',
            field=models.URLField(verbose_name='Código de Programa'),
        ),
    ]