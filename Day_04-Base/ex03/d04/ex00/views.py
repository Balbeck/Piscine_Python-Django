from django.shortcuts import render

# Create your views here.

def index(request):
    """ 
    Vue pour la page Markdown a creer
    context est un dict passe en param de render()
        -> il contient les variables a remplacer dans le template
    """
    context = {
        'titre': 'Ex00 : Markdown Cheatsheet.',
        'nom': 'By Toto 42 🐓'
    }
    return render(request, 'index.html', context=context)
