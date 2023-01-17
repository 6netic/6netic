"""mainsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from cinetic import views


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('cinetic/', include('cinetic.urls')),
    path('l_orchidee/', include('l_orchidee.urls')),
    # path('ciblerie/', include('ciblerie.urls')),
    path('limobooking/', include('limobooking.urls')),
    # path('purbeurre/', include('purbeurre.urls')),
    path('grandpy/', include('grandpy.urls')),
    path('hunting_quizz/', include('hunting_quizz.urls')),
    path('admin/', admin.site.urls),
]