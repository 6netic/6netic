from django.urls import path
from . import views


app_name = 'ciblerie'

urlpatterns = [
    path('index', views.index, name='index'),
    path('ten_meters', views.ten_meters, name='ten_meters'),
]