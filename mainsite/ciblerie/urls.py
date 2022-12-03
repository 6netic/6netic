from django.urls import path
from . import views


app_name = 'ciblerie'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('ten_meters', views.ten_meters, name='ten_meters'),
    path('tests_1', views.tests_1, name='tests_1'),
    path('tests_2', views.tests_2, name='tests_2'),

]