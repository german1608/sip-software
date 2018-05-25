from django.shortcuts import render
from django.views.generic import View
import asignaturas.gestionAsignatura
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    context = {}

    context['pagename'] = 'Dashboard'
    
    return render(request, 'base/blanco.html', context)

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
        