"""
Modulo de python para las pruebas unitarias respecto al modulo de ofertas
de nuestra aplicacion. Se prueban 3 cosas:

* modelos
* vistas
* formularios
"""
# Librerias nativas
import datetime
import json
import time
from io import StringIO

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
# imports de django
from django.test import Client, RequestFactory, SimpleTestCase, TestCase, tag
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import ActionChains

from coordinacion.models import Coordinacion
# Modelos necesarios para las pruebas
from oferta.forms import OfertaForm
from oferta.models import Oferta
from asignaturas.models import Asignatura

# Create your tests here.

class TestUrls(SimpleTestCase):
    """
    Clase que prueba la existencia de los url's vitales para el funcionamiento del sistema
    de ofertas del SIP.
    """

    def test_oferta_url_dasboard(self):
        """
        Verifica la existencia del url 'dashboard'
        """
        reverse('oferta:dashboard')

    def test_oferta_url_anadir(self):
        """
        Verifica la existencia del url 'anadir'
        """
        reverse('oferta:anadir-oferta')

    def test_oferta_url_json(self):
        """
        Verifica la existencia del url 'json'
        """
        reverse('oferta:oferta-json')

    def test_oferta_url_eliminar(self):
        """
        Verifica la existencia del url 'eliminar'
        """
        reverse('oferta:eliminar-oferta', kwargs={'pk': 1})

    def test_oferta_url_descargar(self):
        """
        Verifica la existencia del url 'descargar'
        """
        reverse('oferta:descargar')

    def test_oferta_url_detalle(self):
        """
        Verifica la existencia del url 'detalles'
        """
        reverse('oferta:detalles-oferta', kwargs={'pk': 1})

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

    def test_form_unique(self):
        # Prueba para probar la unicidad de las ofertas respecto a:
        # (anio, trimestre, coordinacio)
        today = datetime.date.today()
        Oferta(trimestre=0, anio=today.year, coordinacion=self.coordinacion).save()
        self.initial['anio'] = today.year
        self.initial['trimestre'] = 0
        form = OfertaForm(self.initial)
        self.assertFalse(form.is_valid())

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

    def test_trimestre_attribute_menos_1(self):
        """El trimestre debe ser un numero del 0 al 2
        0 -> Ene-Mar
        1 -> Abr-Jul
        2 -> Sep-Dic
        Esta validacion pasa en los formularios, pero no en los modelos.
        Estas pruebas van a probar solamente el 3 y el -1 (frontera y esquina, en este caso)
        """
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
        self.helper_test_mixed_to_fail(-1, self.oferta.anio)

    def test_oferta_anio_pasado_trim_tres(self):
        self.helper_test_mixed_to_fail(3, self.oferta.anio)

    def test_oferta_anio_que_viene_trim_menos_1(self):
        self.helper_test_mixed_to_fail(-1, self.oferta.anio)

    def test_oferta_anio_que_viene_trim_tres(self):
        self.helper_test_mixed_to_fail(3, self.oferta.anio)

    def test_oferta_unicity(self):
        """
        Pruebas para la unicidad de la oferta
        """
        # guardamos la oferta en la base de datos
        self.oferta.save()
        with self.assertRaises(IntegrityError):
            # intentamos guardar una identica
            Oferta(
                trimestre=self.oferta.trimestre,
                anio=self.oferta.anio,
                coordinacion=self.oferta.coordinacion,
            ).save()

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
        self.factory = RequestFactory()

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
                'anio': x.anio,
                'urledit': reverse('oferta:detalles-oferta', kwargs={'pk': x.id})
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

    def test_anadir_trimestre_fronteras(self):
        """
        Prueba los trimestres frontera que se le pasaran a la vista
        que crea la oferta. La forma en la que se prueba esto es
        verificando que redirija a donde debe.
        """
        # data que se usara en cada post
        data = {
            'anio': 123,
            'trimestre': 1,
            'coordinacion': self.coordinacion.pk
        }
        # deberia crear la oferta sin ningun problema
        index_route = reverse('oferta:dashboard')
        anadir_route = reverse('oferta:anadir-oferta')
        data['trimestre'] = 0 # frontera
        response = self.client.post(anadir_route, data)
        self.assertRedirects(response, index_route)
        data['trimestre'] = 2 # frontera
        response = self.client.post(anadir_route, data)
        self.assertRedirects(response, index_route)
        self.assertEqual(Oferta.objects.all().count(), 2)

    def test_anadir_trimestre_ya_existente(self):
        """
        Prueba para la vista de crear asignatura, se prueba
        la unicidad
        """
        data = {
            'trimestre': 0,
            'coordinacion': self.coordinacion.pk,
            'anio': 123,
        }
        self.client.post(reverse('oferta:anadir-oferta'), data)
        response = self.client.post(reverse('oferta:anadir-oferta'), data)
        # no deberia redirijir, deberia mostrar la misma pagina
        self.assertEqual(response.status_code, 200)

@tag('selenium')
class TestInterfaceOferta(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        anio_actual = datetime.date.today().year + 1
        self.coordinacion = Coordinacion.objects.create(
            codigo='CI', nombre='Coordinacion 1'
        )
        self.ofertas = [
            Oferta(trimestre=i, anio=j, coordinacion=self.coordinacion)
            for i in range(3) for j in range(anio_actual, anio_actual + 1)
        ]

        self.asignaturas = [
            Asignatura(
                codasig='CO-{}111'.format(i),
                nombre='Asignatura {}'.format(i),
                creditos=i,
                pertenece=self.coordinacion
                )
            for i in range(5)
        ]
        for oferta in self.ofertas: oferta.save()
        for asignatura in self.asignaturas: asignatura.save()

    def test_agregar_oferta_valida(self):
        """
        Test para probar la interfaz con la accion de usuario de crear ofertas.
        La data de este test es valida, y se deberia de cumplir las siguientes condiciones:

        * El numero de ofertas luego de agregar via el form aumenta en 1 tanto en la BD como en la interfaz
        * Deberia mostrar el toastr en la interfaz de color verde
        """
        num_ofertas = Oferta.objects.all().count() # anadimos uno por que el boton de agregar cuenta como cartica

        # Iniciamos el tests haciendo una peticion al url index
        self.selenium.get('%s%s' % (self.live_server_url, reverse('oferta:dashboard')))

        # Verificamos que el numero de contenedores sea num_ofertas + 1
        self.assertEqual(len(self.selenium.find_elements_by_class_name('oferta')), num_ofertas + 1)

        # El flujo de la creacion es:
        # 1) Clickear el boton de anadir ofertas
        add_btn = self.selenium.find_element_by_id('oferta-add')
        add_btn.click()

        # Aqui hay una animacion de 0.5 segundos, asi que para hacer que se tarde
        # selenium esperemos 1 segundo
        time.sleep(1)
        # 2) Llenar los campos solicitados
        form = self.selenium.find_element_by_id('form-oferta')
        trimestre_input = Select(form.find_element_by_name('trimestre'))
        trimestre_input.select_by_value('0')
        anio_input = form.find_element_by_name('anio')
        anio_input.clear()
        anio_input.send_keys('2018')

        # 3) Hacer submit
        form.find_element_by_css_selector('[type=submit]').click()

        # Como es exitosa, debe aparecer las ofertas nuevas en index incluyendo un popup de exito
        self.selenium.find_element_by_id('toast-container')
        self.assertEqual(len(self.selenium.find_elements_by_class_name('oferta')), num_ofertas + 2)
        self.assertEqual(Oferta.objects.all().count(), num_ofertas + 1)

    def test_eliminar_oferta(self):
        """
        Prueba la interfaz mediante la eliminacion
        """
        antes = len(self.ofertas)
        self.selenium.get('%s%s' % (self.live_server_url, reverse('oferta:dashboard')))
        primera_oferta = self.ofertas[0]
        # primero tengo que hacer hover sobre la cartica
        cartica = self.selenium.find_element_by_id('editar-oferta-box-{}'.format(primera_oferta.pk))
        hover = ActionChains(self.selenium).move_to_element(cartica)
        hover.perform()
        time.sleep(0.5)
        # luego tengo que hacer click sobre la equis
        equis = self.selenium.find_element_by_css_selector(
            '[data-url="{}"]'.format(reverse('oferta:eliminar-oferta', kwargs={
                'pk': primera_oferta.pk
            }))
        )
        equis.click()
        # esperamos por el modal
        time.sleep(1)
        eliminar_btn = self.selenium.find_element_by_id('eliminar_oferta_button')
        eliminar_btn.click()
        # verificamos eliminacion
        self.assertEqual(Oferta.objects.all().count(), antes - 1)

    def test_editar_oferta(self):
        """
        Prueba la edicion de la oferta mediante la vista de detalles.
        Casos fronteras sobre el trimestre
        """
        oferta_a_editar = Oferta.objects.create(trimestre=1, anio=2020, coordinacion=self.coordinacion).pk
        self.selenium.get('%s%s' % (self.live_server_url, reverse('oferta:detalles-oferta',kwargs={
            'pk':oferta_a_editar
            }))
        )
        # cliqueamos el boton de edicion
        edit_btn = self.selenium.find_element_by_id('editar')
        edit_btn.click()
        # Buscamos el formulario
        form = self.selenium.find_element_by_css_selector('form')
        # colocamos trimestre 0
        trimestre_input = Select(form.find_element_by_name('trimestre'))
        trimestre_input.select_by_value('0')
        # guardamos
        edit_btn.click()
        time.sleep(1)
        self.assertEqual(Oferta.objects.get(pk=oferta_a_editar).trimestre, 0)
        # iniciamos nuevamente la edicion
        edit_btn.click()
        # trimestre 2
        trimestre_input.select_by_value('2')
        # guardamos
        edit_btn.click()
        time.sleep(1)
        self.assertEqual(Oferta.objects.get(pk=oferta_a_editar).trimestre, 2)

    def test_vincular_asignatura_a_oferta(self):
        """
        Prueba la agregacion de la oferta mediante la vista de detalles.
        Casos frontera sobre la cantidad de asignaturas: todas las asignaturas
        """
        oferta_a_editar = self.ofertas[0].pk
        self.selenium.get('%s%s' % (self.live_server_url, reverse('oferta:detalles-oferta',kwargs={
            'pk':oferta_a_editar
            }))
        )
        # cliqueamos el boton de edicion
        edit_btn = self.selenium.find_element_by_id('editar')
        edit_btn.click()
        # Buscamos las asignaturas
        # primer caso, vincular TODAS
        asignaturas_no_anadidas = self.selenium.find_elements_by_css_selector('#todas-asignaturas .handle')
        destino = self.selenium.find_element_by_css_selector('.tabla-asignaturas-oferta .sortable')
        for asignatura in asignaturas_no_anadidas:
            action_chains = ActionChains(self.selenium)
            action_chains.drag_and_drop(asignatura, destino).perform()
        edit_btn.click()
        time.sleep(1)
        # verificamos que se hayan anadido todas
        self.assertEqual(self.ofertas[0].asignatura.all().count(), len(self.asignaturas))

    def test_vincular_asignatura_a_oferta_eliminar(self):
        """
        Prueba la elimnacion de la oferta mediante la vista de detalles.
        Casos frontera sobre la cantidad de asignaturas: conjunto vacio de ofertas

        """
        # iniciamos la edicion otra vez
        oferta_a_editar = self.ofertas[0].pk
        for asignatura in self.asignaturas:
            self.ofertas[0].asignatura.add(asignatura)

        self.selenium.get('%s%s' % (self.live_server_url, reverse('oferta:detalles-oferta',kwargs={
            'pk':oferta_a_editar
            }))
        )

        edit_btn = self.selenium.find_element_by_id('editar')
        edit_btn.click()
        asignaturas_anadidas = self.selenium.find_elements_by_css_selector('.tabla-asignaturas-oferta .handle')
        destino = self.selenium.find_element_by_css_selector('#todas-asignaturas .sortable')
        for asignatura in asignaturas_anadidas:
            action_chains = ActionChains(self.selenium)
            action_chains.drag_and_drop(asignatura, destino).perform()
        edit_btn.click()
        time.sleep(1)
        # verificamos que se hayan elimnado todas
        self.assertEqual(self.ofertas[0].asignatura.all().count(), 0)

    def test_buscar_asignatura_anadida(self):
        """
        Prueba el buscar sobre las asignaturas anadidas a una oferta
        """
        oferta_a_editar = self.ofertas[0].pk
        for asignatura in self.asignaturas:
            self.ofertas[0].asignatura.add(asignatura)

        self.selenium.get('%s%s' % (self.live_server_url, reverse('oferta:detalles-oferta',kwargs={
            'pk':oferta_a_editar
            }))
        )

        input_elm = self.selenium.find_element_by_id('myInput')
        input_elm.clear()
        input_elm.send_keys('1')
        asignaturas_anadidas = self.selenium.find_elements_by_css_selector('.tabla-asignaturas-oferta li:not([style="display: none;"])')
        # todas las asignaturas tienen 1, asi que deberian estar todas
        self.assertEqual(len(asignaturas_anadidas), len(self.asignaturas))
        input_elm.clear()
        input_elm.send_keys('') # caso frontera, vacio
        asignaturas_anadidas = self.selenium.find_elements_by_css_selector('.tabla-asignaturas-oferta li:not([style="display: none;"])')
        self.assertEqual(len(asignaturas_anadidas), len(self.asignaturas))
        input_elm.clear()
        input_elm.send_keys('ásígnáturá') # caso malicioso, acentos
        asignaturas_anadidas = self.selenium.find_elements_by_css_selector('.tabla-asignaturas-oferta li:not([style="display: none;"])')
        self.assertEqual(len(asignaturas_anadidas), len(self.asignaturas))
        input_elm.clear()
        input_elm.send_keys('3') # caso malicioso, unico
        asignaturas_anadidas = self.selenium.find_elements_by_css_selector('.tabla-asignaturas-oferta li:not([style="display: none;"])')
        self.assertEqual(len(asignaturas_anadidas), 1)
