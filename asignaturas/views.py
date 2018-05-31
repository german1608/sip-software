from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Asignatura
from .forms import AsignaturaForm, HorarioFormset, ProgramaFormset

from django.core import serializers
from django.template.loader import render_to_string
from pprint import pprint

HORARIOS_PREFIX = 'horarios'
PROGRAMAS_PREFIX = 'programas'
class Index(TemplateView):
    template_name = 'asignaturas/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asignaturas'] = Asignatura.objects.all()
        context['pagename'] = 'Asignaturas'
        context['form'] = AsignaturaForm()
        context['formset1'] = HorarioFormset(prefix=HORARIOS_PREFIX)
        context['formset2'] = ProgramaFormset(prefix=PROGRAMAS_PREFIX)
        return context

    def post(self, request, *args, **kwargs):
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


        '''
        Borrar los forms borrados
        '''
        for form1 in formset1.deleted_forms:
            form1.instance.delete()

        for form2 in formset2.deleted_forms:
            form2.instance.delete()

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
        _id = request.POST.get('id', '')
        pprint(request.POST)
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
        if form.is_valid() and formset1.is_valid() and formset2.is_valid():
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
                'valid': True, 'html': ''
            })
        else:
            context['form'] = form
            context['formset1'] = formset1
            context['formset2'] = formset2
            rendered = render_to_string('asignaturas/asignatura_form.html', context=context, request=request)
            return JsonResponse({
                'valid': False,
                'html': rendered
            })

class EditarAsignaturaView(View):
    def get(self, request, *args, **kwargs):
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

'''
Funciones de Gestión de Asignatura
'''
def eliminarAsignatura(codasig):
    try:
        delete_return = Asignatura.objects.get(codasig=codasig).delete()
        print('Se borraron {} asignaturas: {}'.format(delete_return[0], delete_return[1]))
    except Exception as e:
        print(e)


class AsignaturasAsJson(View):
    def get(self, *args, **kwargs):
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
    template_name = 'asignaturas/asignatura_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asignatura = Asignatura.objects.get(id=kwargs['pk'])
        context['asignatura'] = asignatura
        context['programas'] = asignatura.programas.all()
        context['horarios'] = asignatura.horarios.all()
        return context
