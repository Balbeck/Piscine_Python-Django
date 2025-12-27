from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from decouple import config

table_name = 'ex04_movies'

def init(request):
    try:
        conn = psycopg2.connect(
            dbname=config('POSTGRES_DB'),
            user=config('POSTGRES_USER'),
            password=config('POSTGRES_PASSWORD'),
            host='localhost',
            port='5432',
        )
        # print(config('POSTGRES_DB'),
        #     config('POSTGRES_USER'),
        #     config('POSTGRES_PASSWORD'),)
        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            episode_nb INTEGER PRIMARY KEY,
            title VARCHAR(64) UNIQUE NOT NULL,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL
        );
        """
        
        cursor = conn.cursor()
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
        conn.close()
        
        return HttpResponse("OK")
    
    except Exception as e:
        return HttpResponse(f"Erreur : {e}")

def populate(request):
    try:
        conn = psycopg2.connect(
            dbname=config('POSTGRES_DB'),
            user=config('POSTGRES_USER'),
            password=config('POSTGRES_PASSWORD'),
            host='localhost',
            port='5432',
        )

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

        INSERT_DATA = f"""
        INSERT INTO {table_name}
        (
            episode_nb,
            title,
            director,
            producer,
            release_date
        )
        VALUES
        (
            %s, %s, %s, %s, %s
        );
        """

        result = []

        with conn.cursor() as curs:
            for movie in movies:
                try:
                    curs.execute(INSERT_DATA, [
                        movie['episode_nb'],
                        movie['title'],
                        movie['director'],
                        movie['producer'],
                        movie['release_date'],
                    ])
                    result.append(f"OK -> {movie['title']}")
                    conn.commit()
                except psycopg2.DatabaseError as e:
                    conn.rollback()
                    result.append(f'[ {movie['title']} ]: 🚨 {e}')
        return HttpResponse('<br/>'.join(str(i) for i in result))
    except Exception as e:
        return HttpResponse(e)


def display(request):
    try:
        conn = psycopg2.connect(
            dbname=config('POSTGRES_DB'),
            user=config('POSTGRES_USER'),
            password=config('POSTGRES_PASSWORD'),
            host='localhost',
            port='5432',
        )

        SELECT_TABEL = f"""
            SELECT * FROM {table_name};
            """
        
        with conn.cursor() as curs:
            curs.execute(SELECT_TABEL)
            movies = curs.fetchall()

        return render(request, 'ex04/display.html', {'movies': movies})
    
    except Exception as e:
        return HttpResponse('No data available')
 
def remove(request):
    try:
        conn = psycopg2.connect(
            dbname=config('POSTGRES_DB'),
            user=config('POSTGRES_USER'),
            password=config('POSTGRES_PASSWORD'),
            host='localhost',
            port='5432',
        )

        if request.method == 'POST':
            title = request.POST.get('title')
            DELETE_QUERY = f"""
                DELETE FROM {table_name}
                WHERE episode_nb = %s;
                """
            with conn.cursor() as curs:
                curs.execute(DELETE_QUERY, [title])
                conn.commit()

        SELECT_TABEL = f"""
            SELECT * FROM {table_name};
            """
        
        with conn.cursor() as curs:
            curs.execute(SELECT_TABEL)
            movies = curs.fetchall()

        return render(request, 'ex04/remove.html', {'movies': movies})
    
    except Exception as e:
        return HttpResponse(f'Error: {e}')
