from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Oferta
from .forms import OfertaForm

from .models import Oferta


# Create your views here.
def index(request):
    return render(request, 'oferta/index.html')

# Se crea la vista para agregar una nueva oferta a la lista 
class OfertaAgregar(CreateView):
    model = Oferta
    form_class = OfertaForm
    # fields = ['trimestre', 'anio', 'coordinacion']
    success_url = 'success'

def oferta_json(request):
    """Envia informacion sobre las asignaturas como objeto JSON
    """
    ofertas = Oferta.objects.all()

    lista_ofertas = list()

    for oferta in ofertas:
        oferta_detalle = {
            'id' : oferta.id,
            'trimestre' : oferta.get_trimestre_display(),
            'anio' : oferta.anio
        }
        lista_ofertas.append(oferta_detalle)

    return JsonResponse({'data' : lista_ofertas})
