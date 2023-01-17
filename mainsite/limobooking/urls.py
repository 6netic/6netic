from django.urls import path
from . import views


app_name = 'limobooking'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('home', views.home, name='home'),
    path('cancelJourney', views.cancelJourney, name='cancelJourney'),
    path('aeroports', views.aeroports, name='aeroports'),
    path('gares', views.gares, name='gares'),
    path('otherDestination', views.otherDestination, name='otherDestination'),
    path('displayJourney/<str:destination>/', views.displayJourney, name='displayJourney'),
    path('selectJourney', views.selectJourney, name='selectJourney'),
    path('recordJourney', views.recordJourney, name='recordJourney'),
    path('cancelJourney', views.cancelJourney, name='cancelJourney'),

]