from django.test import TestCase
from profesores.models import *
from coordinacion.models import *
from .models import *
from .forms import AsignaturaForm, HorarioForm

import datetime
# Create your tests here.

class Base(TestCase):
    def setUp(self):
        self.profesor = Profesor.objects.create(
            cedula='11111111',
            primer_nombre='Jose',
            primer_apellido='Reinoza',
            carnet='11111111',
            fecha_nacimiento=datetime.date.today()
            )
        self.coordinacion = Coordinacion.objects.create(
            nombre='Computacion',
            codigo='CI'
        )
        self.data = {
            'creditos': 1,
            'codasig': 'AA1111',
            'nombre': 'Asig',
            'profesores': [self.profesor.cedula],
            'pertenece': self.coordinacion.codigo,
            'fecha_de_ejecucion': datetime.date.today(),
            'vista': True
        }

class CreditosTestCase(Base):

    def test_creditos_mayor_cero(self):
        self.data['creditos'] = 1
        form = AsignaturaForm(self.data)
        self.assertTrue(form.is_valid())

    def test_creditos_menor_cero(self):
        self.data['creditos'] = -1
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_creditos_igual_cero(self):
        self.data['creditos'] = 0
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

class CodigoAsignaturaTestCase(Base):

    def test_codigos_minuscula(self):
        self.data['codasig'] = 'ci3715'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_codigo_titulo(self):
        self.data['codasig'] = 'Ci3715'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_codigo_correcto(self):
        self.data['codasig'] = 'CI3715'
        form = AsignaturaForm(self.data)
        self.assertTrue(form.is_valid())

    def test_codigo_intercalado(self):
        self.data['codasig'] = 'cI3715'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_codigo_guiones(self):
        self.data['codasig'] = 'CI-3715'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_codigo_incompleto(self):
        self.data['codasig'] = 'CI371'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_codigo_invalido(self):
        self.data['codasig'] = 'CI37151'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_codigo_incorrecto(self):
        self.data['codasig'] = '1CI3715'
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

class HoraInicioTestCase(Base):
    def setUp(self):
        super(HoraInicioTestCase, self).setUp()
        self.asignatura = Asignatura.objects.create(
            nombre='compu',
            codasig='CI1234',
            creditos=1,
            pertenece=self.coordinacion,
            fecha_de_ejecucion=datetime.date.today(),
            vista=True
        )
        self.asignatura.profesores.add(self.profesor)
        self.asignatura.save()
        self.data = {
            'dia': 1,
            'hora_inicio': 1,
            'hora_final': 2,
            'asignatura': self.asignatura.id
        }

    def test_inicio_igual_final(self):
        self.data['hora_final'] = 1
        self.data['hora_inicio'] = 1
        form = HorarioForm(self.data)
        self.assertFalse(form.is_valid())

    def test_inicio_mayor_final(self):
        self.data['hora_final'] = 1
        self.data['hora_inicio'] = 3
        form = HorarioForm(self.data)
        self.assertFalse(form.is_valid())

    def test_inicio_menor_final(self):
        self.data['hora_inicio'] = 1
        self.data['hora_final'] = 2
        form = HorarioForm(self.data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_rango_valores_horas(self):
        self.data['hora_inicio'] = 0
        self.data['hora_final'] = 1
        form = HorarioForm(self.data)
        self.assertFalse(form.is_valid(), form.errors)

        self.data['hora_inicio'] = 12
        self.data['hora_final'] = 13
        form = HorarioForm(self.data)
        self.assertFalse(form.is_valid(), form.errors)

    def test_rango_valores_dia(self):
        self.data['hora_inicio'] = 1
        self.data['hora_final'] = 2
        self.data['dia'] = -1
        form = HorarioForm(self.data)
        self.assertFalse(form.is_valid(), form.errors)
        self.data['dia'] = 5
        form = HorarioForm(self.data)
        self.assertFalse(form.is_valid(), form.errors)
