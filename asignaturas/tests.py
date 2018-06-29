from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from profesores.models import *
from coordinacion.models import *
from .models import *
from .forms import AsignaturaForm, HorarioForm, HorarioFormset, ProgramaForm
from .views import horario_valido

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

class HorarioTestCase(Base):
    def setUp(self):
        super(HorarioTestCase, self).setUp()
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

    def test_horarios_chocan(self):
        horario1 = Horario.objects.create(dia=1, hora_inicio=2, hora_final=3, asignatura=self.asignatura)
        horario2 = Horario.objects.create(dia=1, hora_inicio=1, hora_final=2, asignatura=self.asignatura)
        self.assertFalse(horario_valido([horario1, horario2]))

    def test_horarios_no_chocan(self):
        horario1 = Horario.objects.create(dia=1, hora_inicio=3, hora_final=4, asignatura=self.asignatura)
        horario2 = Horario.objects.create(dia=1, hora_inicio=1, hora_final=2, asignatura=self.asignatura)
        self.assertTrue(horario_valido([horario1, horario2]))

class FormatoURL(Base):
    
    def setUp(self):
        super(FormatoURL, self).setUp()
        self.asignatura = Asignatura.objects.create(
            creditos=4,
            codasig='PS1111',
            nombre='Modelos Lineales',
            pertenece=self.coordinacion,
            fecha_de_ejecucion=datetime.date.today(),
            vista=False
        )

        self.data = {
            'url': 'https://bitcoin.org/files/bitcoin-paper/bitcoin_es_latam.pdf',
            'asignatura': self.asignatura.id
        }

    def test_url_http(self):
        self.data['url'] = 'http://bitcoin.org/files/bitcoin-paper/bitcoin_es_latam.pdf'
        form = ProgramaForm(self.data)
        self.assertTrue(form.is_valid())

    def test_url_https(self):
        self.data['url'] = 'https://bitcoin.org/files/bitcoin-paper/bitcoin_es_latam.pdf'
        form = ProgramaForm(self.data)
        self.assertTrue(form.is_valid())

    def test_url_other(self):    
        self.data['url'] = 'ssh://bitcoin.org/files/bitcoin-paper/bitcoin_es_latam.pdf'
        form = ProgramaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_url_no_protocol(self):
        self.data['url'] = 'www.bitcoin.org'
        form = ProgramaForm(self.data)
        self.assertFalse(form.is_valid())

    def test_url_no_domain(self):
        self.data['url'] = 'bitcoin'
        form = ProgramaForm(self.data)
        self.assertFalse(form.is_valid())
    def test_url_no_domain(self):
        self.data['url'] = 'bitcoin'
        form = ProgramaForm(self.data)
        self.assertFalse(form.is_valid())

class TestUrls(SimpleTestCase):
    """
    Suite de pruebas para probar la existencia de los urls
    vitales del modulo de asignaturas de SIP
    """
    def test_asig_url_dashboard(self):
        """
        Prueba para la exitencia del url 'dashboard'
        """
        reverse('asignaturas:dashboard')

    def test_asig_url_all_json(self):
        """
        Prueba para la existencia del url 'all-json'
        """
        reverse('asignaturas:all-json')

    def test_asig_url_detalles(self):
        """
        Prueba para la existencia del url 'detalles'
        """
        reverse('asignaturas:detalles', kwargs={'pk': 1})

    def test_asig_url_eliminar(self):
        """
        Prueba para la existencia del url 'eliminar'
        """
        reverse('asignaturas:eliminar-asignatura')

    def test_asig_url_anadir(self):
        """
        Prueba para la existencia del url 'anadir'
        """
        reverse('asignaturas:anadir-asignatura')
