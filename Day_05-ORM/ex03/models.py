from django.db import models

# Create your models here.

class Movies(models.Model):

    title = models.CharField(max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(max_length=32, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)
    
    # Non obligatoire et redondant car par defaut Dj creer table
    # app_name(ex00) _ model_name(movies) minuscule
    # -> ex01_movies
    # class Meta:
    #     db_table = 'ex01_movies'

    def __str__(self) -> str:
        return self.title
