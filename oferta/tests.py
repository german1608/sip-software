"""
Modulo de python para las pruebas unitarias respecto al modulo de ofertas
de nuestra aplicacion. Se prueban 3 cosas:

* modelos
* vistas
* formularios
"""
# imports de django
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import OperationalError
# Modelos necesarios para las pruebas
from oferta.forms import OfertaForm
from coordinacion.models import Coordinacion
from oferta.models import Oferta

# Librerias nativas
import datetime

# Create your tests here.
class TestFormOferta(TestCase):
    """
    Clase que tendra nuestra Suite de pruebas para el formulario.
    En esta clase nada mas se prueba que el anio sea valido,
    pues las validaciones de los choices del trimestre ya las implementa
    los forms de django.
    """
    def setUp(self):
        """
        Método que inicializara la data de muestra para el formulario.
        Crea una coordinación pues una oferta debería estar suscrita a
        una esta.
        """
        self.coordinacion = Coordinacion.objects.create(codigo='CI', nombre='Coordinacion 1')
        self.initial = {
            'coordinacion': self.coordinacion.pk,
            'trimestre': 0,
            'anio': 2018 # anio actual
        }

    def test_form_anio_actual(self):
        # esta data inicial es válida, deberia de ser valido el formulario
        today = datetime.date.today()
        self.initial['anio'] = today.year
        form = OfertaForm(self.initial)
        self.assertTrue(form.is_valid())

    def test_form_anio_menor(self):
        # El formulario no deberia de aceptar anios anteriores al actual
        today = datetime.date.today()
        self.initial['anio'] = today.year - 1
        form = OfertaForm(self.initial)
        self.assertFalse(form.is_valid())

    def test_form_anio_mayor(self):
        # El formulario deberia de aceptar anios posteriores al actual
        today = datetime.date.today()
        self.initial['anio'] = today.year + 1
        form = OfertaForm(self.initial)
        self.assertTrue(form.is_valid())

class TestModelOferta(TestCase):
    """
    A pesar de que con los formularios se pueden crear objetos,
    no quita la posibilidad de crearlos via el ORM de django.
    Estos tests verifican que los campos de cada atributo cumplan
    con los criterios de nuestro ER.
    """
    def setUp(self):
        """
        Esto se ejecuta antes de iniciar cada prueba, lo que permite evitar repeticion de
        codigo innecesaria (DRY!).
        """
        self.coordinacion = Coordinacion.objects.create(codigo='CI', nombre='Coordinacion 1')
        Oferta.objects.all().delete()
        oferta = Oferta()
        oferta.trimestre = 0
        oferta.anio = datetime.date.today().year
        oferta.coordinacion = self.coordinacion
        self.oferta = oferta

        """
        El trimestre debe ser un numero del 0 al 2
        0 -> Ene-Mar
        1 -> Abr-Jul
        2 -> Sep-Dic
        Esta validacion pasa en los formularios, pero no en los modelos.
        Estas pruebas van a probar solamente el 3 y el -1 (frontera y esquina, en este caso)
        """
    def test_trimestre_attribute_menos_1(self):
        # caso esquina: trimestre = -1
        self.oferta.trimestre = -1
        with self.assertRaises(ValidationError):
            self.oferta.save()
        self.assertEqual(Oferta.objects.all().count(), 0)

    def test_trimestre_attribute_tres(self):
        # caso esquina: trimestre = 3
        self.oferta.trimestre = 3
        with self.assertRaises(ValidationError):
            self.oferta.save()
        self.assertEqual(Oferta.objects.all().count(), 0)

    def test_trimestre_attribute_validos(self):
        # caso frontera = 0,1,2
        for i in range(3):
            oferta = Oferta()
            oferta.anio = 2018
            oferta.coordinacion = self.coordinacion
            oferta.trimestre = i
            oferta.save() # no deberia lanzar error
        self.assertEqual(Oferta.objects.all().count(), 3)

        """
        El anio de una oferta debe ser mayor o igual al anio actual.
        El dominio de esta debe ser {x| x >= anio_actual}, por tanto se probara
        para x = anio_actual, x = anio_actual + 1, x = anio_actual - 1.

        Deberia lanzar un ValidationError con los anios_invalidos (anio_actual - 1)
        """
    def test_trimestre_anio_pasado(self):
        # caso esquina: anio pasado
        anio_actual = self.oferta.anio
        self.oferta.anio = anio_actual - 1
        with self.assertRaises(ValidationError):
            self.oferta.save()
        self.assertEqual(Oferta.objects.all().count(), 0)

    def test_trimestre_anio_actual(self):
        # caso frontera: anio actual
        anio_actual = self.oferta.anio
        self.oferta.anio = anio_actual
        self.oferta.save()
        self.assertEqual(Oferta.objects.all().count(), 1)

    def test_trimestre_anio_que_viene(self):
        # caso frontera: anio actual
        anio_actual = self.oferta.anio
        self.oferta.anio = anio_actual
        self.oferta.save()
        self.assertEqual(Oferta.objects.all().count(), 1)
