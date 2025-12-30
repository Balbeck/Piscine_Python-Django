from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Planets, People
import json


def populate(request):
    try:
        json_file_path = 'ex09/ex09_initial_data.json'
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        result = []
        n_planet = 0
        n_people = 0
        
        planet_pk_to_name = {}
        planets_data = []
        people_data = []
        
        for item in data:
            if item['model'] == 'ex09.planets':
                planets_data.append(item)
                planet_pk_to_name[item['pk']] = item['fields']['name']
            elif item['model'] == 'ex09.people':
                people_data.append(item)
        
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
                result.append(f'Error planet 🚨 {fields.get("name")}: {e}')
                continue
        
        result.append(f'✅ Planets: {n_planet} created')
        
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
                
                if created:
                    n_people += 1
                    
            except Exception as e:
                result.append(f'Error person 🚨 {fields.get("name")}: {e}')
                continue
        
        result.append(f'✅ People: {n_people} created')
        
        return HttpResponse('<br/>'.join(result))
    
    except FileNotFoundError:
        return HttpResponse('🚨 Error: ex09_initial_data.json not found')
    except Exception as e:
        return HttpResponse(f'Error: {e}')


def display(request):
    try:
        condition = 'windy'
        # condition = 'arid'
        # condition = 'toto'
        # condition = ''

        people = People.objects.select_related('homeworld').filter(
            homeworld__climate__icontains=condition).order_by('name')
        
        if not people.exists():
            comand_line = f'<br> \' http://localhost:8000/ex09/populate/ \'  First'
            return HttpResponse('No data available, please use the following command line before use:{comand_line}'.format(comand_line=comand_line))
        
        characteristics = []
        for person in people:
            characteristics.append({
                'name': person.name,
                'homeworld': person.homeworld.name if person.homeworld else 'Unknown',
                'climate': person.homeworld.climate if person.homeworld else 'Unknown'
            })
        
        return render(request, 'ex09/display.html', {
            'characteristics': characteristics
        })
    
    except Exception as e:
        return HttpResponse(f'No data available. Error: {e}')
