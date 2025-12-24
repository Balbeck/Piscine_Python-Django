from django.shortcuts import render

# Create your views here.
def django_view(request):
    """Page sur Django et son historique"""
    return render(request, 'ex01/django.html')

def affichage_view(request):
    """Page sur le processus d'affichage d'une page statique"""
    return render(request, 'ex01/affichage.html')

def templates_view(request):
    """Page sur le moteur de templates"""
    context = {
        'items': ['Blocs', 'Boucles for...in', 'Structures if', 'Variables'],
        'show_advanced': True,
    }
    return render(request, 'ex01/templates.html', context)
