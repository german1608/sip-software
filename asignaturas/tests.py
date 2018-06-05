from django.test import TestCase
from profesores.models import *
from coordinacion.models import *
from .forms import AsignaturaForm
from .forms import HorarioForm
from .forms import ProgramaForm

from datetime import date
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
            'vista': True,
            'url': 'http:/'

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

class FechaDeEjecucion(Base):

    def test_fecha_de_ejecucion_menor_a_hoy(self):
        self.data['fecha_de_ejecucion'] = datetime.date.today() - datetime.timedelta(days=1)
                                        #datetime.date(2000, 6, 4)
        form = AsignaturaForm(self.data)
        self.assertTrue(form.is_valid())

    def test_fecha_de_ejecucion_igual_a_hoy(self):
        self.data['fecha_de_ejecucion'] = datetime.date.today()
        form = AsignaturaForm(self.data)
        self.assertTrue(form.is_valid())

    def test_fecha_de_ejecucion_mayor_a_hoy(self):
        self.data['fecha_de_ejecucion'] = datetime.date.today() + datetime.timedelta(days=1)
                                        #datetime.date(2030, 6, 4)
        form = AsignaturaForm(self.data)
        self.assertFalse(form.is_valid())

