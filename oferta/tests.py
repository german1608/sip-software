"""
Modulo de python para las pruebas unitarias respecto al modulo de ofertas
de nuestra aplicacion. Se prueban 3 cosas:

* modelos
* vistas
* formularios
"""
# imports de django
from django.test import TestCase, Client, RequestFactory
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import OperationalError
# Modelos necesarios para las pruebas
from oferta.forms import OfertaForm
from coordinacion.models import Coordinacion
from oferta.models import Oferta

# Librerias nativas
import datetime
import json
from io import StringIO
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

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

    """
    Pruebas esquinas usando ambos atributos
    """

    def helper_test_mixed_to_fail(self, trimestre, anio):
        """
        Funcion de utilidad, como cada test de esquina mixto es basicamente lo mismo se crea esta
        funcion para que varie usando los parametros

        @param trimestre entero que representa el anio (puede ser valido o no)
        @param anio entero que representa el anio (puede ser valido o no)
        """
        self.oferta.trimestre = trimestre
        self.oferta.anio = anio
        with self.assertRaises(ValidationError):
            self.oferta.save()
        self.assertEquals(Oferta.objects.all().count(), 0)

    def test_oferta_anio_pasado_trim_menos_1(self):
        self.helper_test_mixed_to_fail(-1, self.oferta.anio - 1)

    def test_oferta_anio_pasado_trim_tres(self):
        self.helper_test_mixed_to_fail(3, self.oferta.anio - 1)

    def test_oferta_anio_que_viene_trim_menos_1(self):
        self.helper_test_mixed_to_fail(-1, self.oferta.anio + 1)

    def test_oferta_anio_que_viene_trim_tres(self):
        self.helper_test_mixed_to_fail(3, self.oferta.anio + 1)

class TestViewsOferta(TestCase):
    """
    Suite de pruebas para las vistas de el modulo de ofertas. Se usa el cliente integrado
    de django para poder probar cada vista. Recordemos que casi todo es ajax, asi que debe
    probarse con los requests necesarios. El tipo de cosas que se prueban en este Suite son:

    * Existencia de urls vitales del modulo
    * Pruebas de dominio para las vistas que hagan operaciones CRUD sobre la base de datos.

    El modulo de ofertas tiene 3 controladores:
    * anadir (tambien es usado para editar)
    * index
    * json
    """
    def setUp(self):
        """
        Igual que las otras, esta funcion se ejecuta antes de cada test.
        """
        self.coordinacion = Coordinacion.objects.create(nombre='Coordinacion 1', codigo='CI')

    def test_ofertas_index(self):
        """
        Prueba la existencia del index, haciendo un get request
        """
        response = self.client.get(reverse('oferta:dashboard'))
        self.assertEqual(response.status_code, 200)

    def compara_json_realidad(self, ofertas_list):
        """
        Funcion de utilidad para no escribir el mismo test varias veces.

        @param ofertas_list lista de ofertas cuyo tipo de dato es:
        [dict]

        cada dict es

        {
            'id': oferta.id,
            'trimestre': oferta.get_trimestre_display(),
            'anio': oferta.anio,
        }
        """
        expected_list = list(map(
            lambda x: {
                'id': x.id,
                'trimestre': x.get_trimestre_display(),
                'anio': x.anio
            },
            Oferta.objects.all()
        ))
        order_function = lambda x: (x['id'], x['trimestre'], x['anio'])
        ofertas_list.sort(key=order_function)
        expected_list.sort(key=order_function)
        self.assertEqual(ofertas_list, expected_list)

    def test_ofertas_json_empty(self):
        """
        Prueba que el controlador de json funcione de manera adecuada cuando
        no hay ofertas agregadas a la base de datos
        """
        # Realizamos una peticion al url para las ofertas en formato json
        response = self.client.get(reverse('oferta:oferta-json'))
        self.assertEqual(response.status_code, 200)
        ofertas_list = json.loads(response.content.decode('utf-8'))['data']
        self.compara_json_realidad(ofertas_list)
        for i in range(3):
            Oferta(trimestre=i, anio=2018, coordinacion=self.coordinacion).save()

    def test_ofertas_json_non_empty(self):
        for i in range(3):
            Oferta(trimestre=i, anio=2018, coordinacion=self.coordinacion).save()
        response = self.client.get(reverse('oferta:oferta-json'))
        self.assertEqual(response.status_code, 200)
        ofertas_list = json.loads(response.content.decode('utf-8'))['data']
        self.compara_json_realidad(ofertas_list)

    def test_anadir_exists(self):
        """
        Test para probar la existencia del url para la creacion de ofertas.
        """
        response = self.client.get(reverse('oferta:anadir-oferta'))
        self.assertEqual(response.status_code, 200)
