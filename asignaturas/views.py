from django.shortcuts import render
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Asignatura
from .forms import AsignaturaForm, HorarioFormset, ProgramaFormset


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
        

'''
Funciones de Gestión de Asignatura
'''
def eliminarAsignatura(codasig):
    try:
        delete_return = Asignatura.objects.get(codasig=codasig).delete()
        print('Se borraron {} asignaturas: {}'.format(delete_return[0], delete_return[1]))
    except Exception as e:
        print(e)