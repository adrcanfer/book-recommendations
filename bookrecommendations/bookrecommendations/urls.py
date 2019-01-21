"""bookrecommendations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from main import views

urlpatterns = [
    path(r'', views.index),
    path('populate/', views.populate),
    path('book/list/', views.list_book),
    path('book/generate_rating/', views.generate_rating),
    path('admin/', admin.site.urls),
    path('book/search/', views.search),
    path('book/load_rs/', views.load_rs),
    path('book/recommendations/', views.recommendations),
    path('user/register/', views.create_user),
    path('user/login/', views.login),
    path('user/logout/', views.logout),
]
