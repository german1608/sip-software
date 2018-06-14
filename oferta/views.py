from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Oferta
from .forms import OfertaForm

# Create your views here.
def index(request):
    return render(request, 'oferta/index.html')

# Se crea la vista para agregar una nueva oferta a la lista 
class OfertaAgregar(CreateView):
    model = Oferta
    form_class = OfertaForm
    # fields = ['trimestre', 'anio', 'coordinacion']
    success_url = 'success'
