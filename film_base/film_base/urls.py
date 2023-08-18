"""
URL configuration for film_base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, re_path
from webfilm.views import show_movies_template, edit_movies, add_movie, \
    show_person_list_template, show_person_template, add_person_template, \
    search_movie, del_movie, del_person


urlpatterns = [
    path('movies/', show_movies_template, name='movies'),
    path('edit-movie/<int:id>/', edit_movies, name='edit_movie'),
    path('add-movie/', add_movie, name='add_movie'),
    path('del_movie/<int:id>', del_movie, name="del_movie"),
    path('persons/', show_person_list_template, name='persons'),
    path('edit-person/<int:id>/', show_person_template, name='edit_person'),
    path('add-person/', add_person_template, name='add_person'),
    path('del_person/<int:id>', del_person, name="del_person"),
    path('search_movie/', search_movie, name='search_movie'),
]
