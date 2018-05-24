from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}

    context['pagename'] = 'Dashboard'
    
    return render(request, 'base/blanco.html', context)

