from django.urls import path
from . import views


app_name = 'grandpy'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('process', views.process, name='process'),
]