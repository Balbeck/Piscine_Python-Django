from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name=''),
    path('populate/', views.populate, name='populate'),
]
