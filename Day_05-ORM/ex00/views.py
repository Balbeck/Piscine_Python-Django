from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from decouple import config

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
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ex00_movies (
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
