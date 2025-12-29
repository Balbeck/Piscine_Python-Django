from django.shortcuts import render
from django import db
from django.http import HttpResponse
from .models import Movies

# Create your views here.

def populate(request):
    movies = [
            {
                "episode_nb": 1,
                "title": "The Phantom Menace",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "1999-05-19"
            },
            {
                "episode_nb": 2,
                "title": "Attack of the Clones",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2002-05-16"
            },
            {
                "episode_nb": 3,
                "title": "Revenge of the Sith",
                "director": "George Lucas",
                "producer": "Rick McCallum",
                "release_date": "2005-05-19"
            },
            {
                "episode_nb": 4,
                "title": "A New Hope",
                "director": "George Lucas",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1977-05-25"
            },
            {
                "episode_nb": 5,
                "title": "The Empire Strikes Back",
                "director": "Irvin Kershner",
                "producer": "Gary Kurtz, Rick McCallum",
                "release_date": "1980-05-17"
            },
            {
                "episode_nb": 6,
                "title": "Return of the Jedi",
                "director": "Richard Marquand",
                "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum",
                "release_date": "1983-05-25"
            },
            {
                "episode_nb": 7,
                "title": "The Force Awakens",
                "director": "J. J. Abrams",
                "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
                "release_date": "2015-12-11"
            }
        ]
    
    result = []
    for movie in movies:
        try:
            Movies.objects.create(
                episode_nb=movie['episode_nb'],
                title=movie['title'],
                opening_crawl=movie.get('opening_crawl', None),
                director=movie['director'],
                producer=movie['producer'],
                release_date=movie['release_date'],
            )
            result.append(f'OK -> ✅ {movie['title']}')
        except db.Error as e:
            result.append(f'[ {movie['title']} ]: 🚨 {e}')

    return HttpResponse("<br/>".join(str(i) for i in result))

    

def display(request):
    try:
        movies = Movies.objects.all()
        if not movies.exists():
            return HttpResponse("No data available")

        columns = [field.name for field in Movies._meta.get_fields()]
        movies_data = []
        for movie in movies:
            movie_values = [getattr(movie, col) for col in columns]
            movies_data.append(movie_values)

        return render(request, 'ex07/display.html', {
            'columns': columns,
            'movies': movies_data
        })
    
    except Exception as e:
        return HttpResponse("No data available")
 

def update(request):
    try:

        # Gere UPDATE
        if request.method == 'POST':
            episode_nb = request.POST.get('episode_nb')
            opening_crawl = request.POST.get('opening_crawl')
            
            #Update
            movie = Movies.objects.get(episode_nb=episode_nb)
            movie.opening_crawl = opening_crawl
            # methode save() permet auto maj du champ Date dans model:
            #  - > updated = models.DateTimeField(auto_now=True)
            movie.save()

        # Gere le Form
        movies = Movies.objects.all()
        # movies = Movies.objects.values_list('episode_nb', 'title')
        print(movies)

        return render(request, 'ex07/update.html', {'movies': movies})
    
    except Exception as e:
        return HttpResponse('No data available')
        # return HttpResponse(f'Error: {e}')