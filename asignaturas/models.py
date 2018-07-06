"""
Modelos del modulo de asignaturas. Tiene solamente 3

- Asignatura
- Horario
- ProgramaAsignatura

Horario y ProgramaAsignatura no deben existir sin estar relacionados a una Asignatura
"""

import datetime

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, URLValidator
from django.db import models

from coordinacion.models import Coordinacion
from profesores.models import Profesor

class Asignatura(models.Model):
    """
    Entidad Asignatura. Tiene los atributos necesarios para representar
    una asignatura en la vida real.

    - codasig
    - nombre
    - creditos
    - profesores (relacion de muchos a muchos con Profesor)
    - pertenece (relacion de muchos a muchos con Coordinacion)
    - fecha_de_ejecucion
    - vista
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    codasig = models.CharField(max_length=10, unique=True,
        verbose_name='Código de Asignatura', validators=[
            RegexValidator(
                regex='^[A-Z]{2}[0-9]{4}$',
                message='Formato de código incorrecto. Ej: CO3121',
                code='codigo_invalido'
            )
        ]
    )
    creditos = models.PositiveSmallIntegerField(verbose_name='Créditos')
    profesores = models.ManyToManyField(Profesor, verbose_name='Profesores',
        related_name='profesores')
    pertenece = models.ForeignKey(Coordinacion, verbose_name='Coordinación',
        related_name='asignaturas', on_delete=models.CASCADE)
    fecha_de_ejecucion = models.DateField(default=datetime.date.today, verbose_name='Fecha de ejecución')
    vista = models.BooleanField(default=False, verbose_name='Asignatura Vista')

    def __str__(self):
        """Forma de devolver la asignatura."""
        return self.codasig + ": " + self.nombre

class ProgramaAsignatura(models.Model):
    """
    Entidad ProgramaAsignatura. Tiene los atributos necesarios para modelar
    un programa de una asignatura de la vida real.
    - url (por los momentos)
    - asignatura (foranea a la asignatura)
    """
    url = models.CharField(max_length=500, validators=[URLValidator()], verbose_name='Código de Programa')
    asignatura = models.ForeignKey(Asignatura,
        related_name='programas', on_delete=models.CASCADE, verbose_name='Asignatura')

    def __str__(self):
        """  """
        return self.codigo + ": " + str(self.asignatura.nombre)
    class Meta:
        """  """
        unique_together = ('url', 'asignatura')

def hora_valida(x):
    """ Verificación de que el rango para una hora debe ser entre 1 y 12"""
    if not (1 <= x <= 12):
        raise ValidationError('{} no está entre 1 y 12'.format(x))

class Horario(models.Model):
    """
    Entidad Horario. Permite representar un horario vinculado a una oferta.
    - dia (como entero, luego se hace el mapeo)
    - hora_inicio y hora_final (entre 1 y 12)
    - asignatura (foranea a una Asignatura)

    Para evitar desperdicios en la bd, la tupla completa de atributos debe ser unica.
    """
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
        """Muestra un formato para dia con horario de inicio y fin."""
        return self.get_dia_display() + ": " + str(self.hora_inicio) + "-" + str(self.hora_final)

    class Meta:
        """ Hace unica la tupla."""
        unique_together = ('asignatura', 'hora_inicio', 'hora_final', 'dia')
