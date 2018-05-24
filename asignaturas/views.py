from django.shortcuts import render
from django.views.generic import *
from asignaturas.models import *
from coordinacion.models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json
import re

# Create your views here.

class Busqueda(View):
	def get(self, request):

		return render(self.request, 'base/blanco.html')

	def post(self, request):

		# Expresion regular para hacer match con el input
		regex = re.compile('[A-Z][A-Z]-[0-9]{4}')
		
		# Diccionario con los datos de respuesta
		datos_respuesta = {}


		submit = request.POST.get('input')
		busqueda = Asignatura.objects.get(codasig=submit)

		# Verificamos si la busqueda es exitosa o no.
		if busqueda != None:
			# Verificamos si la busqueda cumple con la sintaxis de un codigo de asignatura.
			if not regex.match(busqueda.codasig):
				raise ValidationError(u'%s no cumple con la sintaxis de codigo de asignatura' % busqueda)
			else:
				datos_respuesta['nombre'] = busqueda.nombre
				datos_respuesta['codasig'] = busqueda.codasig
				datos_respuesta['creditos'] = busqueda.creditos
				print(type(busqueda.profesores))
				datos_respuesta['nombre_coordinacion'] = busqueda.pertenece.nombre
				datos_respuesta['codigo_coordinacion'] = busqueda.pertenece.codigo
		else:
			datos_respuesta['status_code'] = 404
			datos_respuesta['error'] = 'La busqueda fue infructuosa'	

		jsonBusqueda = JsonResponse(datos_respuesta) 

		return jsonBusqueda


