"""
Vistas del modulo de Ofertas de SIP. Permite la interaccion
del usuario con el servidor.
"""

import datetime

from django.core import serializers
from django.db.models import Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View, generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from asignaturas.models import Asignatura
from coordinacion.models import Coordinacion

from .forms import AsignaturaFormset, OfertaForm
from .models import Oferta
from .render import Render


# Create your views here.
def index(request):
    """
    Esta es la unica peticion que hace el navegador directamente.
    El resto es puro AJAX.
    """
    anos = [x for x in reversed(range(2000, (datetime.datetime.now().year)+20))]
    choices = Oferta.OFERTA_TRIMESTRE_CHOICES
    context = {
        'anos': anos,
        'choices': choices,
        'pagename': 'Ofertas'
    }
    return render(request, 'oferta/index.html', context)


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

# Se crea la vista para agregar una nueva oferta a la lista
class OfertaAgregar(AjaxableResponseMixin, CreateView):
    """
    Vista en forma de Clase que facilita la creacion al extender
    la vista generica CreateView. Dado que la creacion de objetos
    en el servidor es un patron repetitivo, django incorpora ciertas
    herramientas para facilitar este trabajo y reducir el codigo
    que hace lo mismo siempre.

    Tambien extiende de AjaxableResponseMixin,
    que nos permite facilitar el uso de esta via ajax.
    """
    model = Oferta
    template_name = 'oferta/oferta-form.html'
    form_class = OfertaForm
    success_url = 'success'

    def get_initial(self):
        initial = super(OfertaAgregar, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['coordinacion'] = Coordinacion.objects.all().first()
        # etc...
        return initial

# Se crea la vista para editar una oferta de la lista
class OfertaEditar(AjaxableResponseMixin, UpdateView):
    """
    Vista en forma de Clase que facilita la edicion de ofertas al extender
    la vista generica UpdateView. Tambien hereda de AjaxableResponseMixin
    para facilitar el uso de esta vista via AJAX.
    """
    # Esto realiza la conexion con el html
    model = Oferta
    template_name = 'oferta/oferta-form.html'
    form_class = OfertaForm


class DetallesOferta(generic.DetailView):
    """
    Esta clase es una vista que va a mostrar los detalles de una oferta,
    esto incluye las asignaturas, los horarios, etc
    """
    model = Oferta
    template_name = 'oferta/detalle.html'


    def get_context_data(self, **kwargs):
        context = super(DetallesOferta, self).get_context_data(**kwargs)
        oferta = Oferta.objects.get(pk=self.kwargs['pk'])
        asignaturas_oferta = oferta.asignatura.all()
        asignaturas_disponibles = [asignatura for asignatura in Asignatura.objects.all() if not asignatura in asignaturas_oferta]
        context['oferta'] = oferta
        context['form'] = OfertaForm(instance=oferta)
        context['formset'] = AsignaturaFormset(prefix='asignaturas', queryset=Asignatura.objects.none())
        context['asignaturas'] = asignaturas_oferta
        context['pagename'] = oferta.get_trimestre_display() + " " + str(oferta.anio)
        context['lista_asignaturas'] = asignaturas_disponibles
        return context

    def post(self, request, **kwargs):
        pk = self.kwargs['pk']
        oferta = Oferta.objects.get(pk=pk)
        form = OfertaForm(self.request.POST, instance=oferta)
        formset = AsignaturaFormset(self.request.POST, prefix='asignaturas')
        if form.is_valid() and formset.is_valid():
            form.save()
            form.instance.asignatura.set([])
            for form1 in formset:
                oferta.asignatura.add(form1.cleaned_data['id'])
            form.save()
            return JsonResponse({'errors': '', 'valid': True})
        return JsonResponse({'errors': form.errors, 'valid': False})      

# Esta funcion esta encargada de enviar con formato json la informacion de
# todas las ofertas que se han anadido a la base de datos
def oferta_json(request):
    """Envia informacion sobre las asignaturas como objeto JSON
    """
    if request.method == 'GET':
        if not Oferta.objects.all():
            return JsonResponse({'data': []})

        trim_inicio = request.GET.get('trim_inicio', Oferta.TRIMESTRE_ENEMAR)
        trim_final = request.GET.get('trim_final', Oferta.TRIMESTRE_SEPDIC)

        anio_inicio = request.GET.get('anio_inicio', min_anio_oferta())
        # Checkeamos si no es null
        anio_inicio = anio_inicio if anio_inicio else min_anio_oferta()

        anio_final = request.GET.get('anio_final', max_anio_oferta())
        # checkeamos si no es null
        anio_final = anio_final if anio_final else max_anio_oferta()

        ofertas = Oferta.objects.filter(trimestre__gte=trim_inicio) \
                .filter(trimestre__lte=trim_final).filter(anio__gte=anio_inicio) \
                .filter(anio__lte=anio_final).order_by('anio').order_by('trimestre')

    mapper = (lambda obj: {
        'trimestre': obj.get_trimestre_display(),
        'anio': obj.anio,
        'id': obj.pk,
        'urledit': reverse('oferta:detalles-oferta', kwargs={'pk': obj.pk})
    })

    return JsonResponse({'data' : list(map(mapper, ofertas)) })

class EliminarOferta(DeleteView):
    """
    Elimina una oferta utilizando como apoyo la vista generica de eliminacion de Django.

    El metodo get se sobreescribe para que la pagina no redirija al template por defecto
    de la vista genérica de Django cuando se solicita la eliminación de una oferta. En este caso,
    la llamada mediante AJAX con método GET a esta vista retornará informacion del objeto que se
    quiere eliminar.

    El metodo delete se sobreescribe para evadir la redireccion que hace DeleteView
    hacia success_url. Así, se devuelve una respuesta JSON indicando el estado de la
    operacion.
    """
    model = Oferta
    success_url = reverse_lazy('oferta:oferta-eliminacion-exitosa')

    def get(self, request, *args, **kwargs):
        # Obtenemos la oferta mediante el metodo get_object provisto
        # por la vista de django
        oferta = self.get_object()

        # Retornamos informacion para llenar el modal de eliminacion
        # con la informacion de la oferta que estamos eliminando.
        return JsonResponse({
            'trimestre' : oferta.get_trimestre_display(),
            'anio' : oferta.anio,
            'coordinacion' : oferta.coordinacion.nombre,
        })

    def delete(self, request, *args, **kwargs):
        """
        Llama al metodo delete() en el objeto buscado y luego devuelve
        una respuesta JSON indicando el estado de la operacion.
        """
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'ok': True})

# Vista para descargar las ofertas como PDF
class DescargarOfertasView(View):
    """
    Vista que genera el PDF tomando los filtros adecuados.
    Toma en cuenta tanto trimestres de inicio y fin como
    anios de inicio y fin.
    """
    def get(self, request, *args, **kwargs):
        if not Oferta.objects.all():
            return Render.render('oferta/ofertas.pdf.html', {})

        trim_inicio = request.GET.get('trim_inicio', Oferta.TRIMESTRE_ENEMAR)
        trim_final = request.GET.get('trim_final', Oferta.TRIMESTRE_SEPDIC)

        anio_inicio = request.GET.get('anio_inicio', min_anio_oferta())
        # Checkeamos si no es null
        anio_inicio = anio_inicio if anio_inicio else min_anio_oferta()

        anio_final = request.GET.get('anio_final', max_anio_oferta())
        # checkeamos si no es null
        anio_final = anio_final if anio_final else max_anio_oferta()


        # Conjunto de ofertas que cumplen con los criterios especificados
        ofertas = Oferta.objects.filter(trimestre__gte=trim_inicio) \
            .filter(trimestre__lte=trim_final).filter(anio__gte=anio_inicio) \
            .filter(anio__lte=anio_final).order_by('anio').order_by('trimestre')
        if ofertas:
            context = {
                'ofertas': ofertas,
                'trim_inicio': ofertas.first().get_trimestre_display(),
                'trim_final': ofertas.last().get_trimestre_display(),
                'anio_inicio': anio_inicio,
                'anio_final': anio_final
            }
        else:
            context = {}

        return Render.render('oferta/ofertas.pdf.html', context)

# Función que retorna el mayor de los años de las ofertas guardadas
def max_anio_oferta():
    return Oferta.objects.all().aggregate(Max('anio')).get('anio__max')

# Función que retorna el menor de los años de las ofertas guardadas
def min_anio_oferta():
    return Oferta.objects.all().aggregate(Min('anio')).get('anio__min')
