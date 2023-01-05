from django.urls import path
from . import views
from django.contrib import admin


app_name = 'hunting_quizz'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.index, name='index'),
    path('add_question', views.add_question, name='add_question'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
]