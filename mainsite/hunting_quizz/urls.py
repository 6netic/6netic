from django.urls import path
from . import views
from django.contrib import admin

app_name = 'hunting_quizz'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('apprentissage', views.apprentissage, name='apprentissage'),
    path('normal_quizz', views.normal_quizz, name='normal_quizz'),
    path('add_question', views.add_question, name='add_question'),
    path('assisted_quizz', views.assisted_quizz, name='assisted_quizz'),
]
