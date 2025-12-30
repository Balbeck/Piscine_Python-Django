from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate, name='ex09-populate'),
    path('display/', views.display, name='ex09-display'),
]
