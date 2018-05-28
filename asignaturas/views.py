from django.shortcuts import render
from django.views.generic import View
import asignaturas.gestionAsignatura
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from asignaturas.models import *
from coordinacion.models import *
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json
import re


def index(request):
    context = {}

    context['pagename'] = 'Dashboard'
    
    return render(request, 'asignaturas/index.html', context)

# Vista para eliminar asignatura
class EliminarAsignaturaView(TemplateView):
    template_name = 'asignaturas/eliminar_asignatura.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()

        # workaround para DELETE methods
        if method == 'delete':
            return self.delete(*args, **kwargs)

        return super(EliminarAsignaturaView, self).dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        asignaturas.gestionAsignatura.eliminarAsignatura(self.request.POST.get('codasig'))

        # Redirige al inicio por ahora
        return HttpResponseRedirect(reverse('asignaturas:index'))
        

class IndexView(View):
    
    template_name = 'asignaturas/index.html'


    def get(self, request):

        # Expresion regular para hacer match con el input
        regex = re.compile('[A-Z][A-Z][0-9]{4}')
        
        # Diccionario con los datos de respuesta
        datos_respuesta = {}


        submit = request.GET.get('input')
        
        encontrado = False

        for asignatura in Asignatura.objects.all():
            if asignatura.codasig == submit:
                encontrado = True

        busqueda = None     
        if encontrado:
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
                jsonBusqueda = JsonResponse(datos_respuesta) 
                return jsonBusqueda    
        else:
            datos_respuesta['status_code'] = 404
            datos_respuesta['error'] = 'La busqueda fue infructuosa'    


        return render(self.request, "asignaturas/index.html")    