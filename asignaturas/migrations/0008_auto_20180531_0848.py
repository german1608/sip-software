# Generated by Django 2.0.5 on 2018-05-31 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asignaturas', '0007_auto_20180531_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programaasignatura',
            name='url',
            field=models.URLField(unique=True, verbose_name='Código de Programa'),
        ),
    ]