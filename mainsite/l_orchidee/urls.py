from django.urls import path
from . import views
from django.contrib import admin


app_name = 'l_orchidee'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('display_form', views.display_form, name='display_form'),
    path('check_variables', views.check_variables, name='check_variables'),
    path('extract_in_pref', views.extract_in_pref, name='extract_in_pref'),
    path('extract_in_vill', views.extract_in_vill, name='extract_in_vill'),
    path('check_date_and_is_registered', views.check_date_and_is_registered, name='check_date_and_is_registered'),
    path('insert_tour', views.insert_tour, name='insert_tour'),
    path('display_tour', views.display_tour, name='display_tour'),
    path('save_comment', views.save_comment, name='save_comment'),
    path('validate_line', views.validate_line, name='validate_line'),
    path('view_planning', views.PlanningView.as_view(), name='view_planning'),
    path('insert_planning', views.insert_planning, name='insert_planning'),
    path('connect', views.connect, name='connect'),
    path('disconnect', views.disconnect, name='disconnect'),
    path('modifyPassword', views.modifyPassword, name='modifyPassword'),
    path('clean_db', views.clean_db, name="clean_db"),
]