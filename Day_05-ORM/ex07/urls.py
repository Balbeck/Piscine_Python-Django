from django.urls import path
from . import views

urlpatterns = [
    path('populate/', views.populate, name='ex05-populate'),
    path('display/', views.display, name='ex05-display'),
    path('update/', views.update, name='ex05-update'),
]
