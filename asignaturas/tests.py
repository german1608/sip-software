from django.test import TestCase
from profesores.models import *
from coordinacion.models import *
from .forms import AsignaturaForm

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