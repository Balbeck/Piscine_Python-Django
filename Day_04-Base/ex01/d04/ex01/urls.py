from django.urls import path
from . import views

app_name = 'ex01'

urlpatterns = [
    path('django/', views.django_view, name='django'),
    path('affichage/', views.affichage_view, name='affichage'),
    path('templates/', views.templates_view, name='templates'),
]
