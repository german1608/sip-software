"""
Vistas del modulo de asignaturas.
EN esta vista se hace la interaccion
usuario-sistema.
"""

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import View
from django.views.generic.base import TemplateView

from .forms import AsignaturaForm, HorarioFormset, ProgramaFormset
from .models import Asignatura

HORARIOS_PREFIX = 'horarios'
PROGRAMAS_PREFIX = 'programas'
class Index(TemplateView):
    """
    Vista de la página de asignaturas. Tiene dos funciones principales:
    - Mostrar la pagina principal de asignaturas con la tabla de asignaturas.
    - Manejar el método POST para crear una nueva asignatura.

    Adicionalmente contiene una funcion auxiliar para determinar si un horario
    introducido de una asignatura es válido (Ej: colocar 5-3)
    """
    template_name = 'asignaturas/index.html'

    def get_context_data(self, **kwargs):
        """
        Obtenemos todo el contexto necesario para renderizar
        la lista de asignaturas y el formulario de una asignatura
        de modo que no haya que recargar la pagina.
        """
        asignatura = self.request.GET.get('codasig')
        context = super(Index, self).get_context_data(**kwargs)
        context['asignaturas'] = Asignatura.objects.all()
        context['pagename'] = 'Asignaturas'
        context['form'] = AsignaturaForm()
        context['formset1'] = HorarioFormset(prefix=HORARIOS_PREFIX)
        context['formset2'] = ProgramaFormset(prefix=PROGRAMAS_PREFIX)
        context['asignatura'] = Asignatura.objects.filter(codasig=asignatura)
        if len(context['asignatura']) == 0:
            context['activar_modal'] = False
        else:
            context['asignatura'] = Asignatura.objects.get(codasig=asignatura)
            context['activar_modal'] = True
        return context

    def post(self, request, *args, **kwargs):
        """
        Metodo que maneja la creacion de una nueva asignatura al
        hacer un post sobre el formulario de asignaturas.
        """
        id = request.POST.get('id', '')
        try:
            # Vemos si ya la asignatura existe
            asignatura = Asignatura.objects.get(id=id)
            form = AsignaturaForm(request.POST, instance=asignatura)
            formset1 = HorarioFormset(request.POST, instance=asignatura, prefix=HORARIOS_PREFIX)
            formset2 = ProgramaFormset(request.POST, instance=asignatura, prefix=PROGRAMAS_PREFIX)
        except Exception as e:
            # Crear asignatura
            form = AsignaturaForm(request.POST)
            formset1 = HorarioFormset(request.POST, prefix=HORARIOS_PREFIX)
            formset2 = ProgramaFormset(request.POST, prefix=PROGRAMAS_PREFIX)

        context = self.get_context_data()
        """
        Validamos los distintos formularios completados al crear
        una asignatura y se hacen las conexiones a nivel de base
        de datos entre la asignatura, el horario y el programa.
        """
        if form.is_valid() and formset1.is_valid() and formset2.is_valid():
            form.save()
            for instance in formset1.save(commit=False):
                instance.asignatura = form.instance
                instance.save()
            for instance in formset2.save(commit=False):
                instance.asignatura = form.instance
                instance.save()

        else:
            context['form'] = form
            context['formset1'] = formset1
            context['formset2'] = formset2
        """
        Aqui eliminamos los forms borrados.
        
        """
        for form1 in formset1.deleted_forms:
            form1.instance.delete()

        for form2 in formset2.deleted_forms:
            form2.instance.delete()

        return render(request, self.template_name, context)
      
    def horario_valido(self,lista):
        """

        Esta funcion se encarga de la determinación de colisiones
        en la lista de horarios.
        Cuando se obtiene el valor de falso significa que existe una colisión.

        """
        for i in lista:
            for x in lista:
                if i!=x:
                    if i.dia==x.dia:
                        if (i.hora_inicio>=x.hora_inicio and i.hora_inicio<=x.hora_final) or (i.hora_final>=x.hora_inicio and i.hora_final<=x.hora_final) or (i.hora_inicio>x.hora_inicio and i.hora_final<x.hora_final) or (i.hora_inicio<x.hora_inicio and i.hora_final>x.hora_final):
                            return False

        return True


"""
Aquí se encuentra la vista para eliminar una asignatura.

"""

class EliminarAsignaturaView(TemplateView):
    """
    Vista que maneja la eliminación de asignaturas.
    """
    template_name = 'asignaturas/eliminar_asignatura.html'

    def get_context_data(self, **kwargs):
        """Renderiza la data necesaria para la eliminación de una asignatura"""
        context = super().get_context_data(**kwargs)
        return context

    def dispatch(self, *args, **kwargs):
        """
        Maneja el despacho que hace la vista detectando el tipo de
        solicitud realizada
        """
        method = self.request.POST.get('_method', '').lower()

        # workaround para DELETE methods
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(EliminarAsignaturaView, self).dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Esta llamada se realiza si el despacho de la vista determina
        que se desa eliminar una asignatura. Se invoca a la funcion
        que elimina las asignaturas y se retorna una respuesta.
        """
        codasig = self.request.POST.get('codasig')
        Asignatura.objects.get(codasig=codasig).delete()
        return JsonResponse({'ok': True})

def horario_valido(lista):
    """
    Funcion que verifica si una lista de ofertas satisface que no chocan horarios entre si

    @param lista [Horario] Lista de objetos de tipo oferta
    @returns bool retorna true ssi la lista satisface que no chocan los horarios.

    @examples:
    lista = [
        Horario(dia=1, hora_inicio=1, hora_final=2),
        Horario(dia=1, hora_inicio=1, hora_final=3)
    ]
    self.assertFalse(horario_valido(lista)) # no falla
    lista = [
        Horario(dia=1, hora_inicio=1, hora_final=2),
        Horario(dia=2, hora_inicio=1, hora_final=3)
    ]
    self.assertTrue(horario_valido(lista)) # tampoco
    """
    for i in lista:
        for x in lista:
            if i!=x:
                if i.dia==x.dia:
                    if (i.hora_inicio>=x.hora_inicio and i.hora_inicio<=x.hora_final) or \
                    (i.hora_final>=x.hora_inicio and i.hora_final<=x.hora_final) or \
                    (i.hora_inicio>x.hora_inicio and i.hora_final<x.hora_final) or \
                    (i.hora_inicio<x.hora_inicio and i.hora_final>x.hora_final):
                        return False
    return True

def horas_validas(lista):
    """
    Determinar la validez de un horario introducido.
    Un horario se considera invalido si no sigue el
    formato de horarios de la USB (1-2, 3-4) etc.

    @param lista [Horario] Lista de objetos de tipo Horario
    @returns boolean True ssi (paratodo x| x in lista : x.hora_inicio < x.hora_final)
    """
    for i in lista:
        if i.hora_inicio >= i.hora_final:
            return False
    return True

class AnadirAsignaturaView(View):
    """
    Clase ayudante del manejo de añadir asignatura.
    """
    def get(self, request, *args, **kwargs):
        """ nos trae los formularios con los detalles de la asignatura"""
        _id = request.GET.get('id', '')
        try:
            # Vemos si ya la asignatura existe
            asignatura = Asignatura.objects.get(id=_id)
            form = AsignaturaForm(instance=asignatura)
            formset1 = HorarioFormset(instance=asignatura, prefix=HORARIOS_PREFIX)
            formset2 = ProgramaFormset(instance=asignatura, prefix=PROGRAMAS_PREFIX)
        except Exception as e:
            # Crear asignatura
            form = AsignaturaForm()
            formset1 = HorarioFormset(prefix=HORARIOS_PREFIX)
            formset2 = ProgramaFormset(prefix=PROGRAMAS_PREFIX)
        context = {
            'form': form,
            'formset1': formset1,
            'formset2': formset2
        }
        rendered = render_to_string('asignaturas/asignatura_form.html', context=context, request=request)
        data = rendered
        return JsonResponse(data, safe=False)

    def post(self, request, *args, **kwargs):
        """ Creacion o actualizacion de la asignatura"""
        _id = request.POST.get('id', '')
        try:
            # Vemos si ya la asignatura existe
            asignatura = Asignatura.objects.get(id=_id)
            form = AsignaturaForm(request.POST, instance=asignatura)
            formset1 = HorarioFormset(request.POST, instance=asignatura, prefix=HORARIOS_PREFIX)
            formset2 = ProgramaFormset(request.POST, instance=asignatura, prefix=PROGRAMAS_PREFIX)
        except Exception as e:
            # Crear asignatura
            form = AsignaturaForm(request.POST)
            formset1 = HorarioFormset(request.POST, prefix=HORARIOS_PREFIX)
            formset2 = ProgramaFormset(request.POST, prefix=PROGRAMAS_PREFIX)

        context = {}
        """ Se guardan en una lista los formularios de horarios """
        horarios = [form1.instance for form1 in formset1]

        if form.is_valid() and formset1.is_valid()\
         and formset2.is_valid() and horario_valido(horarios)\
         and horas_validas(horarios):
            form.save()
            for instance in formset1.save(commit=False):
                instance.asignatura = form.instance
                instance.save()
            for instance in formset2.save(commit=False):
                instance.asignatura = form.instance
                instance.save()
            '''
            Borrar los forms borrados
            '''
            for form1 in formset1.deleted_forms:
                form1.instance.delete()

            for form2 in formset2.deleted_forms:
                form2.instance.delete()
            return JsonResponse({
                'valid': True, 'html': '', 'errors': []
            })
        else:
            errors = []
            context['form'] = form
            context['formset1'] = formset1
            context['formset2'] = formset2
            if form.errors:
                errors.append([form.errors, '#info-pan'])

            if form.non_field_errors():
                for err in form.non_field_errors():
                    errors.append([str(err), '#info-pan'])

            for form1 in formset1:
                if form1.errors:
                    for err in form1.errors:
                        errors.append([form1.errors[err] + str(form1.instance), '#hora-pan'])

            for form2 in formset2:
                if form2.errors:
                    errors.append([form2.errors, '#prog-pan'])
                    for err in form2.errors:
                        errors.append([err, '#prog-pan'])
                if form2.non_field_errors():
                    for err in form2.non_field_errors():
                        errors.append([str(err), '#hora-pan'])

            if (not horario_valido(horarios)):
                errors.append(['Hay horarios solapados', '#hora-pan'])

            if (not horas_validas(horarios)):
                errors.append(['Hay hora de inicio mayor a hora final', '#hora-pan'])

            rendered = render_to_string('asignaturas/asignatura_form.html', context=context, request=request)
            return JsonResponse({
                'valid': False,
                'html': rendered,
                'errors': errors
            })

class EditarAsignaturaView(View):
    """
    Permite renderizar el formulario de añadir una asignatura con
    los datos de una asignatura existente para crear una vista
    de edición de una asignatura.
    """
    def get(self, request, *args, **kwargs):
        """ 
        Se obtiene la asignatura a editar, se busca en la base
        de datos y se toman instancias de los formularios de
        asignaturas para llevarlos a la vista.
        """
        pk = request.GET.get('id', '')
        asig = Asignatura.objects.get(pk=pk)
        context = {
            'form': AsignaturaForm(instance=asig),
            'formset1': HorarioFormset(instance=asig, prefix=HORARIOS_PREFIX),
            'formset2': ProgramaFormset(instance=asig, prefix=PROGRAMAS_PREFIX)
        }
        rendered = render_to_string('asignaturas/asignatura_form.html', context=context, request=request)
        data = rendered
        return JsonResponse(data, safe=False)


class AsignaturasAsJson(View):
    """
    Clase que devuelve la lista de asignaturas al ser llamada con método GET
    utilizando AJAX.
    """
    def get(self, *args, **kwargs):
        """ Obtiene los detalles de la asignatura"""
        asignaturas = list(map(
            lambda x: [
                '''<a href="#"
                class="nombre-asignatura"
                onclick="obtenerAsignatura(this, '{url}', false);"
                >{nombre}</a>'''.format(
                    nombre=x['nombre'],
                    url=reverse('asignaturas:detalles', kwargs={'pk': x['id']}),
                    codasig=x['codasig']
                ),
                x['codasig'],
                x['creditos'],
                x['fecha_de_ejecucion']],
            Asignatura.objects.all()
            .values('nombre', 'codasig', 'creditos', 'fecha_de_ejecucion', 'id')
        ))
        return JsonResponse({'data': asignaturas})

class AsignaturaDetallesView(TemplateView):
    """
    Obtener el detalle de una asignatura: datos básicos,
    horarios y programas, para mostrarlos en la vista de
    detalle de una asignatura.
    """
    template_name = 'asignaturas/asignatura_details.html'

    def get_context_data(self, **kwargs):
        """
        Obtiene los datos de los contextos: asignatura; programas; horarios.
        """
        context = super().get_context_data(**kwargs)
        asignatura = Asignatura.objects.get(id=kwargs['pk'])
        context['asignatura'] = asignatura
        context['programas'] = asignatura.programas.all()
        context['horarios'] = asignatura.horarios.all()
        return context

class Ofertas(TemplateView):
    """
    Vista para las ofertas
    """
    template_name = 'oferta/index.html'

    def get_context_data(self, **kwargs):
        """
        Obtiene los datos del contexto.
        """
        context = super().get_context_data(**kwargs)
        return context
