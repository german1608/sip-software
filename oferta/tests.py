"""
Modulo de python para las pruebas unitarias respecto al modulo de ofertas
de nuestra aplicacion. Se prueban 3 cosas:

* modelos
* vistas
* formularios
"""

from django.test import TestCase
from oferta.forms import OfertaForm
from coordinacion.models import Coordinacion
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
