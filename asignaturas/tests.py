from django.test import TestCase
from .forms import AsignaturaForm
# Create your tests here.

class CreditosTestCase(TestCase):

	def test_creditos_mayor_cero(self):
		form = AsignaturaForm(initial={'creditos': 1})
		self.assertTrue(form.is_valid())

	def test_creditos_menor_cero(self):
		form = AsignaturaForm(initial={'creditos': -1})
		self.assertFalse(form.is_valid())

	def test_creditos_igual_cero(self):
		form = AsignaturaForm(initial={'creditos': 0})
		self.assertFalse(form.is_valid())