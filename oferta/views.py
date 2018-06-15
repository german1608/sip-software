from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views import View
from .models import Oferta
from .forms import OfertaForm
from coordinacion.models import Coordinacion
import datetime


from .models import Oferta
from django.db.models import Max, Min

from .render import Render

from pprint import pprint

# Create your views here.
def index(request):
    anos = [x for x in reversed(range(2000, (datetime.datetime.now().year)+20))]
    return render(request, 'oferta/index.html', {'anos': anos})

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

# Esta funcion esta encargada de enviar con formato json la informacion de
# todas las ofertas que se han anadido a la base de datos
def oferta_json(request, mesi=0, anoi=0, mesf=0, anof=0):
    """Envia informacion sobre las asignaturas como objeto JSON
    """

    def mes_a_trimestre(mes):
        if (1 < mes) and (mes <= 3):
            return 0
        if (4 < mes ) and (mes <=8):
            return 1
        return 2

    ofertas = Oferta.objects.all()

    lista_ofertas = list()

    if (mesi != 0 and anoi != 0 and mesf != 0 and anof != 0):
        for oferta in ofertas:
            if (anoi <= oferta.anio) and (oferta.anio <= anof):
                if (anoi == oferta.anio and oferta.trimestre < mes_a_trimestre(mesi)):
                    continue
                if (anof == oferta.anio and oferta.trimestre > mes_a_trimestre(mesf)):
                    continue    
                oferta_detalle = {
                    'id' : oferta.id,
                    'trimestre' : oferta.get_trimestre_display(),
                    'anio' : oferta.anio
                }
                lista_ofertas.append(oferta_detalle)
    else:     
        for oferta in ofertas:
            oferta_detalle = {
                'id' : oferta.id,
                'trimestre' : oferta.get_trimestre_display(),
                'anio' : oferta.anio
            }
            lista_ofertas.append(oferta_detalle)

    return JsonResponse({'data' : lista_ofertas})

# Vista para descargar las ofertas como PDF
class DescargarOfertasView(View):
    def get(self, request, *args, **kwargs):
        trim_inicio = request.GET.get('trim_inicio', Oferta.TRIMESTRE_ENEMAR)
        trim_final = request.GET.get('trim_final', Oferta.TRIMESTRE_SEPDIC)
        anio_inicio = request.GET.get('anio_inicio', min_anio_oferta())
        anio_final = request.GET.get('anio_final', max_anio_oferta())

        # Conjunto de ofertas que cumplen con los criterios especificados
        ofertas = Oferta.objects.filter(trimestre__gte=trim_inicio) \
            .filter(trimestre__lte=trim_final).filter(anio__gte=anio_inicio) \
            .filter(anio__lte=anio_final).order_by('anio').order_by('trimestre')

        context = {
            'ofertas': ofertas,
            'trim_inicio': ofertas.first().get_trimestre_display(),
            'trim_final': ofertas.last().get_trimestre_display(),
            'anio_inicio': anio_inicio,
            'anio_final': anio_final
        }

        pprint(context)

        return Render.render('oferta/ofertas.pdf.html', context)

# Función que retorna el mayor de los años de las ofertas guardadas
def max_anio_oferta():
    return Oferta.objects.all().aggregate(Max('anio')).get('anio__max')

# Función que retorna el menor de los años de las ofertas guardadas
def min_anio_oferta():
    return Oferta.objects.all().aggregate(Min('anio')).get('anio__min')
