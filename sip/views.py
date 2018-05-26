from django.shortcuts import render

def index(request):
    context = {}

    context['pagename'] = 'Dashboard'
    
    return render(request, 'base/blanco.html', context)