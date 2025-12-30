from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('populate/', views.populate, name='populate'),
]
