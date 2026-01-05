from django.shortcuts import render
from django.http import HttpResponse
from ex10.models import Movies, People, Planets
import json
import os


def populate(request):
    # return HttpResponse('[ Populate ]Nothing Yet Bro 👊.html')
    try:
        json_file_path = 'ex10/ex10_initial_data.json'
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        result = []
        n_planet = 0
        n_people = 0
        n_movies = 0
        
        # Dict pour mapper PK aux planet name
        planet_pk_to_name = {}
        
        planets_data = []
        people_data = []
        movies_data = []
        
        for item in data:
            if item['model'] == 'ex10.planets':
                planets_data.append(item)
                planet_pk_to_name[item['pk']] = item['fields']['name']
            elif item['model'] == 'ex10.people':
                people_data.append(item)
            elif item['model'] == 'ex10.movies':
                movies_data.append(item)
        
        for item in planets_data:
            try:
                fields = item['fields']
                
                planet, created = Planets.objects.update_or_create(
                    name=fields['name'],
                    defaults={
                        'climate': fields.get('climate'),
                        'diameter': fields.get('diameter'),
                        'orbital_period': fields.get('orbital_period'),
                        'population': fields.get('population'),
                        'rotation_period': fields.get('rotation_period'),
                        'surface_water': fields.get('surface_water'),
                        'terrain': fields.get('terrain'),
                    }
                )
                
                if created:
                    n_planet += 1
                    
            except Exception as e:
                result.append(f'❌ Error planet {fields.get("name")}: {e}')
                continue
        
        result.append(f'✅ Planets: {n_planet} created')
        
        people_pk_to_obj = {}  # Pour mapper les PK aux People
        
        for item in people_data:
            try:
                fields = item['fields']
                homeworld = None
                homeworld_pk = fields.get('homeworld')
                
                if homeworld_pk and homeworld_pk in planet_pk_to_name:
                    planet_name = planet_pk_to_name[homeworld_pk]
                    try:
                        homeworld = Planets.objects.get(name=planet_name)
                    except Planets.DoesNotExist:
                        result.append(f'⚠️ Planet "{planet_name}" not found for {fields["name"]}')
                
                person, created = People.objects.update_or_create(
                    name=fields['name'],
                    defaults={
                        'birth_year': fields.get('birth_year'),
                        'gender': fields.get('gender'),
                        'eye_color': fields.get('eye_color'),
                        'hair_color': fields.get('hair_color'),
                        'height': fields.get('height'),
                        'mass': fields.get('mass'),
                        'homeworld': homeworld,
                    }
                )
                
                # Stock Object pour ManyToMany
                people_pk_to_obj[item['pk']] = person
                
                if created:
                    n_people += 1
                    
            except Exception as e:
                result.append(f'❌ Error person {fields.get("name")}: {e}')
                continue
        
        result.append(f'✅ People: {n_people} created')
        
        for item in movies_data:
            try:
                fields = item['fields']
                characters_pks = fields.get('characters', [])
                
                movie, created = Movies.objects.update_or_create(
                    episode_nb=item['pk'],
                    defaults={
                        'title': fields['title'],
                        'opening_crawl': fields.get('opening_crawl'),
                        'director': fields['director'],
                        'producer': fields['producer'],
                        'release_date': fields['release_date'],
                    }
                )
                
                # Set People a Movies ManyToMany
                if characters_pks:
                    characters = [people_pk_to_obj[pk] for pk in characters_pks if pk in people_pk_to_obj]
                    movie.characters.set(characters)
                
                if created:
                    n_movies += 1
                    
            except Exception as e:
                result.append(f'❌ Error movie {fields.get("title")}: {e}')
                continue
        
        result.append(f'✅ Movies: {n_movies} created')
        
        planets_count = Planets.objects.count()
        people_count = People.objects.count()
        movies_count = Movies.objects.count()
        
        response = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Populate Success</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: #f4f4f4;
                }}
                .container {{
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{ color: #28a745; }}
                .stats {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .stats ul {{
                    list-style: none;
                    padding: 0;
                }}
                .stats li {{
                    padding: 10px;
                    margin: 5px 0;
                    background: white;
                    border-left: 4px solid #007bff;
                }}
                .log {{
                    background: #fff3cd;
                    padding: 15px;
                    border-radius: 4px;
                    margin: 20px 0;
                    font-size: 14px;
                    max-height: 200px;
                    overflow-y: auto;
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 24px;
                    background: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                a:hover {{ background: #0056b3; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✅ Données chargées avec succès !</h1>
                
                <div class="stats">
                    <h3>📊 Total dans la base de données :</h3>
                    <ul>
                        <li><strong>🪐 Planètes :</strong> {planets_count}</li>
                        <li><strong>👤 Personnages :</strong> {people_count}</li>
                        <li><strong>🎬 Films :</strong> {movies_count}</li>
                    </ul>
                </div>
                
                <div class="log">
                    <h3>📝 Log d'insertion :</h3>
                    {'<br>'.join(result)}
                </div>
                
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(response)
    
    except FileNotFoundError:
        return HttpResponse('❌ Erreur : Le fichier ex10_initial_data.json est introuvable.', status=404)
    except json.JSONDecodeError as e:
        return HttpResponse(f'❌ Erreur : Le fichier JSON est invalide. {e}', status=400)
    except Exception as e:
        return HttpResponse(f'❌ Erreur lors du chargement des données : {e}', status=500)




def display(request):
    # return HttpResponse('[ Display ] Nothing Yet Bro 👊.html')

    genders = People.objects.values_list('gender', flat=True).distinct().order_by('gender')
    results = []
    
    if request.GET:
        min_date = request.GET.get('min_date')
        max_date = request.GET.get('max_date')
        diameter = request.GET.get('diameter')
        gender = request.GET.get('gender')
        
        # Utilise 'prefetch_related' pour build table intermediairepour le ManyToMany
        query = Movies.objects.prefetch_related('characters', 'characters__homeworld').all()
        
        if min_date:
            query = query.filter(release_date__gte=min_date)
        
        if max_date:
            query = query.filter(release_date__lte=max_date)
        
        if diameter:
            query = query.filter(characters__homeworld__diameter__gt=int(diameter))
        
        if gender:
            query = query.filter(characters__gender=gender)
        
        for movie in query.distinct():
            for character in movie.characters.all():
                if gender and character.gender != gender:
                    continue
                if diameter and (not character.homeworld or character.homeworld.diameter <= int(diameter)):
                    continue
                
                results.append({
                    'movie_title': movie.title,
                    'release_date': movie.release_date,
                    'character_name': character.name,
                    'gender': character.gender,
                    'planet_name': character.homeworld.name if character.homeworld else 'Unknown',
                    'diameter': character.homeworld.diameter if character.homeworld else 0,
                })
    
    context = {
        'genders': genders,
        'results': results,
    }
    
    return render(request, 'ex10/display.html', context)
