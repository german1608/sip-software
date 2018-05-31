from django.db import models
from django.core.exceptions import ValidationError

from coordinacion.models import Coordinacion
from profesores.models import Profesor
# Create your models here.

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codasig = models.CharField(max_length=10, primary_key=True,
        verbose_name='Código de Asignatura')
    creditos = models.PositiveSmallIntegerField(verbose_name='Créditos')
    profesores = models.ManyToManyField(Profesor, verbose_name='Profesores',
        related_name='profesores')
    pertenece = models.ForeignKey(Coordinacion, verbose_name='Coordinación',
        related_name='asignaturas', on_delete=models.CASCADE)

    def __str__(self):
        return self.codasig + ": " + self.nombre

class ProgramaAsignatura(models.Model):
    url = models.URLField(verbose_name='Código de Programa', unique=True)
    asignatura = models.ForeignKey(Asignatura,
        related_name='programas', on_delete=models.CASCADE, verbose_name='Asignatura')

    def __str__(self):
        return self.codigo + ": " + str(self.asignatura.nombre)
    class Meta:
        unique_together = ('url', 'asignatura')

def hora_valida(x):
    if not (1 <= x <= 12):
        raise ValidationError('{} no está entre 1 y 12'.format(x))

class Horario(models.Model):
    HORARIO_LUNES = 0
    HORARIO_MARTES = 1
    HORARIO_MIERCOLES = 2
    HORARIO_JUEVES = 3
    HORARIO_VIERNES = 4
    HORARIO_DIA_CHOICES = (
        (HORARIO_LUNES, 'Lunes'),
        (HORARIO_MARTES, 'Martes'),
        (HORARIO_MIERCOLES, 'Miércoles'),
        (HORARIO_JUEVES, 'Jueves'),
        (HORARIO_VIERNES, 'Viernes'),
    )
    dia = models.PositiveSmallIntegerField(choices=HORARIO_DIA_CHOICES,
        verbose_name='Día de la semana')
    hora_inicio = models.PositiveIntegerField(validators=[hora_valida],
        verbose_name='Hora Inicio')
    hora_final = models.PositiveIntegerField(validators=[hora_valida],
        verbose_name='Hora Final')
    asignatura = models.ForeignKey(Asignatura, verbose_name='Asignatura',
        related_name='horarios', on_delete=models.CASCADE)

    def __str__(self):
        return self.determinarFecha(self.dia) + ": " + str(self.hora_inicio) + "-" + str(self.hora_final)

    def determinarFecha(self, numero):
        if numero == 0:
            return 'Lunes'
        elif numero == 1:
            return 'Martes' 
        elif numero == 2:
            return 'Miercoles'
        elif numero == 3:
            return 'Jueves'
        elif numero == 4:
            return 'Viernes'
       
    class Meta:
        unique_together = ('asignatura', 'hora_inicio', 'hora_final', 'dia')
