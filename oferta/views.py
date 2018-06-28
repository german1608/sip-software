from pprint import pprint

from django.db.models import Max, Min
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views import generic
from .models import Oferta
from .forms import OfertaForm
from coordinacion.models import Coordinacion
import datetime

from django.core import serializers

from .forms import OfertaForm
from .models import Oferta

from .render import Render

from pprint import pprint

from django.views.generic.detail import DetailView

# Create your views here.
def index(request):
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
    model = Oferta
    template_name = 'oferta/oferta-form.html'
    form_class = OfertaForm
    # fields = ['trimestre', 'anio', 'coordinacion']
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
    # Esto realiza la conexion con el html 
    model = Oferta
    template_name = 'oferta/oferta-form.html'
    form_class = OfertaForm
    

'''
    Esta funcion es una vista que va a mostrar los detalles de una oferta, 
    esto incluye las asignaturas, los horarios, etc
'''
class DetailView(generic.DetailView):
    model = Oferta
    template_name = 'oferta/detalles-oferta.html'
# def detalles_ofertas(request, oferta_id):
#     print(oferta_id)
#     oferta = Oferta.objects.get(pk=oferta_id)
#     return render(request, 'oferta/detalles-oferta.html', {'oferta': oferta})


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
        'id': obj.pk
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

        pprint(request.GET)

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

        pprint(context)

        return Render.render('oferta/ofertas.pdf.html', context)

# Función que retorna el mayor de los años de las ofertas guardadas
def max_anio_oferta():
    return Oferta.objects.all().aggregate(Max('anio')).get('anio__max')

# Función que retorna el menor de los años de las ofertas guardadas
def min_anio_oferta():
    return Oferta.objects.all().aggregate(Min('anio')).get('anio__min')



def detallesOferta(request):

    return render(request, 'oferta/detalle.html', {})

