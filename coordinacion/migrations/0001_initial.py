# Generated by Django 2.0.5 on 2018-05-21 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coordinacion',
            fields=[
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
    ]