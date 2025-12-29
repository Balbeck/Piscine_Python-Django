from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from decouple import config
import io

planets_table_name = 'ex08_planets'
people_table_name = 'ex08_people'

def get_db_connection():
    conn = psycopg2.connect(
        dbname=config('POSTGRES_DB'),
        user=config('POSTGRES_USER'),
        password=config('POSTGRES_PASSWORD'),
        host='localhost',
        port='5432',
    )
    return conn



def init(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        create_planets_table_query = f"""
        CREATE TABLE IF NOT EXISTS {planets_table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            climate VARCHAR,
            diameter INTEGER,
            orbital_period INTEGER,
            population BIGINT,
            rotation_period INTEGER,
            surface_water REAL,
            terrain VARCHAR(128)
        );
        """

        create_people_table_query = f"""
        CREATE TABLE IF NOT EXISTS {people_table_name} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(64) UNIQUE NOT NULL,
            birth_year VARCHAR(32),
            gender VARCHAR(32),
            eye_color VARCHAR(32),
            hair_color VARCHAR(32),
            height INTEGER,
            mass REAL,
            homeworld VARCHAR(64),
            FOREIGN KEY (homeworld) REFERENCES {planets_table_name}(name)
        );
        """

        cursor.execute(create_planets_table_query)
        cursor.execute(create_people_table_query)

        conn.commit()
        cursor.close()
        conn.close()

        return HttpResponse("OK")
    
    except Exception as e:
        return HttpResponse(f"Erreur : {e}")



def populate(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        result = []
        
        # [ Planets ]
        try:
            with open('ex08/subject_files/planets.csv', 'r', encoding='utf-8') as f:
                # Remplace NULL par \N (format Postgress)
                content = f.read().replace('NULL', '\\N').replace('\t0\t', '\t\\N\t')
                
                # Créer un objet StringIO pour copy_from
                string_buffer = io.StringIO(content)
                
                cursor.copy_from(
                    string_buffer,
                    planets_table_name,
                    sep='\t',
                    null='\\N',
                    columns=('name', 'climate', 'diameter', 'orbital_period', 
                            'population', 'rotation_period', 'surface_water', 'terrain')
                )
                conn.commit()
                result.append('OK - planets.csv ✅')
                
        except Exception as e:
            conn.rollback()
            result.append(f'Error planets: 🚨 {e}')
        
        # [ People ]
        try:
            with open('ex08/subject_files/people.csv', 'r', encoding='utf-8') as f:
                content = f.read().replace('NULL', '\\N')
                
                # Remplacer ',' par '.'  
                lines = content.split('\n')
                cleaned_lines = []
                for line in lines:
                    if line:
                        parts = line.split('\t')
                        if len(parts) >= 7:
                            parts[6] = parts[6].replace(',', '.')
                        cleaned_lines.append('\t'.join(parts))
                
                string_buffer = io.StringIO('\n'.join(cleaned_lines))
                
                cursor.copy_from(
                    string_buffer,
                    people_table_name,
                    sep='\t',
                    null='\\N',
                    columns=('name', 'birth_year', 'gender', 'eye_color', 
                            'hair_color', 'height', 'mass', 'homeworld')
                )
                conn.commit()
                result.append('OK - people.csv ✅')
                
        except Exception as e:
            conn.rollback()
            result.append(f'Error people: 🚨 {e}')
        
        cursor.close()
        conn.close()
        
        return HttpResponse('<br/>'.join(result))
    
    except Exception as e:
        return HttpResponse(f'Error: {e}')



def display(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        condition = 'windy'
        # condition = 'arid'
        # condition = 'toto'
        # condition = ''
        sql_join_query = f"""
            SELECT
                p.name, p.homeworld, pl.climate
            FROM
                ex08_people p
            JOIN
                ex08_planets pl ON p.homeworld = pl.name
            WHERE
                pl.climate LIKE '%%{condition}%%'
            ORDER BY
                p.name ASC;
        """
        cursor.execute(sql_join_query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not results:
            return HttpResponse('No data available')

        return render(request, 'ex08/display.html', { 'characteristics': results })
    
    except Exception as e:
        # return HttpResponse(f'Error: {e}')
        return HttpResponse('No data available')
