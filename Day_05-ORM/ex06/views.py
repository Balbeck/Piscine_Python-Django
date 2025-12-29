from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from decouple import config

table_name = 'ex06_movies'

def get_db_connection():
    conn = psycopg2.connect(
        dbname=config('POSTGRES_DB'),
        user=config('POSTGRES_USER'),
        password=config('POSTGRES_PASSWORD'),
        host='localhost',
        port='5432',
    )
    # print(config('POSTGRES_DB'),
    #     config('POSTGRES_USER'),
    #     config('POSTGRES_PASSWORD'),
    # )

    return conn

def init(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            episode_nb INTEGER PRIMARY KEY,
            title VARCHAR(64) UNIQUE NOT NULL,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)

        # Creer la fonction  Sql trigger permit par Postgress
        create_trigger_fct = """
        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated = now();
            NEW.created = OLD.created;
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
        cursor.execute(create_trigger_fct)
        
        # Creer le trigger sur la Table
        create_trigger = f"""
        DROP TRIGGER IF EXISTS update_films_changetimestamp ON {table_name};
        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
        ON {table_name} FOR EACH ROW EXECUTE PROCEDURE
        update_changetimestamp_column();
        """
        cursor.execute(create_trigger)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return HttpResponse("OK")
    
    except Exception as e:
        return HttpResponse(f"Erreur : {e}")

def populate(request):
    try:
        conn = get_db_connection()

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
        return HttpResponse(f'Error: {e}')


def display(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        get_table_query = f"SELECT * FROM {table_name};"
        cursor.execute(get_table_query)
        
        # Veut afficher dynamiquement display.html sans connaitre taille, colonnes de la table a afficher
        # Grace a cursor.description, récupérer les noms des colonnes
        columns = [desc[0] for desc in cursor.description]
        movies = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if not movies:
            return HttpResponse("No data available")
        
        return render(request, 'ex06/display.html', {
            'columns': columns,
            'movies': movies
        })
    
    except Exception as e:
        # return HttpResponse(f'Error: {e}')
        return HttpResponse('No data available')
 
def update(request):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Gere UPDATE
        if request.method == 'POST':
            episode_nb = request.POST.get('episode_nb')
            opening_crawl = request.POST.get('opening_crawl')
            
            update_query = f"""
            UPDATE {table_name}
            SET opening_crawl = %s
            WHERE episode_nb = %s;
            """
            
            cursor.execute(update_query, [opening_crawl, episode_nb])
            conn.commit()

        # Gere le Form
        SELECT_TABEL = f"""
            SELECT * FROM {table_name};
            """
        cursor.execute(SELECT_TABEL)
        movies = cursor.fetchall()

        cursor.close()
        conn.close()

        return render(request, 'ex06/update.html', {'movies': movies})
    
    except Exception as e:
        return HttpResponse('No data available')
        # return HttpResponse(f'Error: {e}')
