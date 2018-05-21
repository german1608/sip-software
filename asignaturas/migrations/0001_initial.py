# Generated by Django 2.0.5 on 2018-05-21 15:08

import asignaturas.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coordinacion', '0001_initial'),
        ('profesores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('codasig', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='Código de Asignatura')),
                ('creditos', models.PositiveSmallIntegerField(verbose_name='Créditos')),
                ('pertenece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaturas', to='coordinacion.Coordinacion', verbose_name='Coordinación')),
                ('profesores', models.ManyToManyField(related_name='profesores', to='profesores.Profesor', verbose_name='Profesores')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.PositiveSmallIntegerField(choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes')], verbose_name='Día de la semana')),
                ('hora_inicio', models.PositiveIntegerField(validators=[asignaturas.models.hora_valida], verbose_name='Hora Inicio')),
                ('hora_final', models.PositiveIntegerField(validators=[asignaturas.models.hora_valida], verbose_name='Hora Inicio')),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='horarios', to='asignaturas.Asignatura', verbose_name='Asignatura')),
            ],
        ),
        migrations.CreateModel(
            name='ProgramaAsignatura',
            fields=[
                ('codigo', models.CharField(max_length=6, primary_key=True, serialize=False, verbose_name='Código de Programa')),
                ('asignatura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programas', to='asignaturas.Asignatura', verbose_name='Asignatura')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='programaasignatura',
            unique_together={('codigo', 'asignatura')},
        ),
        migrations.AlterUniqueTogether(
            name='horario',
            unique_together={('asignatura', 'hora_inicio', 'hora_final', 'dia')},
        ),
    ]
