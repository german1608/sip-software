from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Asignatura
from .forms import AsignaturaForm, HorarioFormset, ProgramaFormset

from django.core import serializers
from django.template.loader import render_to_string


class Index(TemplateView):
    template_name = 'asignaturas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asignaturas'] = Asignatura.objects.all()
        context['pagename'] = 'Asignaturas'
        context['form'] = AsignaturaForm()
        context['formset1'] = HorarioFormset()
        context['formset2'] = ProgramaFormset()
        return context

    def post(self, request, *args, **kwargs):
        codasig = request.POST.get('codasig', '')
        try:
            # Vemos si ya la asignatura existe
            asignatura = Asignatura.objects.get(codasig=codasig)
            form = AsignaturaForm(request.POST, instance=asignatura)
            formset1 = HorarioFormset(request.POST, instance=asignatura)
            formset2 = ProgramaFormset(request.POST, instance=asignatura)
        except Exception as e:
            # Crear asignatura
            form = AsignaturaForm(request.POST)
            formset1 = HorarioFormset(request.POST)
            formset2 = ProgramaFormset(request.POST)

        context = self.get_context_data()

        if form.is_valid() and formset1.is_valid() and formset2.is_valid():
            form.save()
            for instance in formset1.save(commit=False):
                instance.asignatura = form.instance
                instance.save()
            for instance in formset2.save(commit=False):
                instance.asignatura = form.instance
                instance.save()
        else:
            print(form.errors)
            print(formset1.errors)
            print(formset2.errors)
            context['form'] = form
            context['formset1'] = formset1
            context['formset2'] = formset2
        return render(request, self.template_name, context)


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
        eliminarAsignatura(self.request.POST.get('codasig'))

        # Redirige al inicio por ahora
        return HttpResponseRedirect(reverse('asignaturas:dashboard'))
        
class AnadirAsignaturaView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': AsignaturaForm(),
            'formset1': HorarioFormset(),
            'formset2': ProgramaFormset()
        }
        rendered = render_to_string('asignaturas/asignatura_form.html', context=context, request=request)
        data = rendered
        return JsonResponse(data, safe=False)

class EditarAsignaturaView(View):
    def get(self, request, *args, **kwargs):
        codasig = request.GET.get('codasig', '')
        asig = Asignatura.objects.get(codasig=codasig)
        context = {
            'form': AsignaturaForm(instance=asig),
            'formset1': HorarioFormset(instance=asig),
            'formset2': ProgramaFormset(instance=asig)
        }
        rendered = render_to_string('asignaturas/asignatura_form.html', context=context, request=request)
        data = rendered
        return JsonResponse(data, safe=False)

'''
Funciones de Gestión de Asignatura
'''
def eliminarAsignatura(codasig):
    try:
        delete_return = Asignatura.objects.get(codasig=codasig).delete()
        print('Se borraron {} asignaturas: {}'.format(delete_return[0], delete_return[1]))
    except Exception as e:
        print(e)

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
