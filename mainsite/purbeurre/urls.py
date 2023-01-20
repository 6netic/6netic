from django.urls import path
from . import views


app_name = 'purbeurre'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('legal', views.legal, name='legal'),
    path('search', views.search, name='search'),
    path('detail/<int:product_id>', views.detail, name='detail'),
    path('saveprd/', views.saveprd, name='saveprd'),
	path('showfavourites', views.showfavourites, name='showfavourites'),
    path('account', views.account, name='account'),
    path('register', views.register, name='register'),
	path('connect', views.connect, name='connect'),
	path('disconnect', views.disconnect, name='disconnect'),
	path('modifypassword', views.modifypassword, name='modifypassword'),
]

