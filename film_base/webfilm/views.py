
# Description: This Django web application allows users to manage a collection of movies. Users can view a list of movies,
# search for specific movies based on various criteria such as title, director, and genre, add new movies to the collection,
# edit existing movie details including title, year, director, and rating, as well as delete movies from the collection.
# The application also supports adding and managing information about people involved in movie production, such as directors,
# screenwriters, and actors.


from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from webfilm.models import Movie, Person, Genre, PersonMovie

from django.views import View


def show_movies_template(request):
    # Retrieve the sort_option value from the POST request or session
    sort_option = request.POST.get('sort_option', request.session.get('sorted','0'))

    # Sorting logic based on user's choice
    if sort_option == '1':
        movies = Movie.objects.order_by('-rating')  # Sort by descending rating
    elif sort_option == '2':
        movies = Movie.objects.order_by('rating')   # Sort by ascending rating
    else:
        movies = Movie.objects.order_by('year')     # Sort by year

    # Save sort_option value to session
    request.session['sorted'] = sort_option

    context = {
        "movies": movies
    }
    return render(request, "movies.html", context)

def search_movie(request):
    if request.method == "POST":
        title = request.POST.get('title')
        director_first_name = request.POST.get('director_first_name')
        director_last_name = request.POST.get('director_last_name')
        screenplay_first_name = request.POST.get('screenplay_first_name')
        screenplay_last_name = request.POST.get('screenplay_last_name')
        year_from = request.POST.get('year_from')
        year_to = request.POST.get('year_to')
        genre = request.POST.get('genre')
        rating_from = request.POST.get('rating_from')
        rating_to = request.POST.get('rating_to')
        actor_first_name = request.POST.get('actor_first_name')
        actor_last_name = request.POST.get('actor_last_name')

        # Initialize movies queryset
        movies = Movie.objects.all()
        any_filter_applied = False  # Initialize flag to track if any filter is applied

        # Filter by movie title
        if title:
            movies = movies.filter(title__icontains=title)
            any_filter_applied = True

        # Filter by director's first name and last name
        if director_first_name:
            movies = movies.filter(director__first_name__icontains=director_first_name)
            any_filter_applied = True
        if director_last_name:
            movies = movies.filter(director__last_name__icontains=director_last_name)
            any_filter_applied = True

        # Filter by screenplay writer's first name and last name
        if screenplay_first_name:
            movies = movies.filter(screenplay__first_name__icontains=screenplay_first_name)
            any_filter_applied = True
        if screenplay_last_name:
            movies = movies.filter(screenplay__last_name__icontains=screenplay_last_name)
            any_filter_applied = True

        # Filter by production year
        if year_from and year_to:
            movies = movies.filter(year__range=(year_from, year_to))
            any_filter_applied = True

        # Filter by movie rating
        if rating_from and rating_to:
            movies = movies.filter(rating__range=(rating_from, rating_to))
            any_filter_applied = True

        # Filter by genres
        if genre:
            genre = [g.replace(" ", "") for g in genre.split(',')]
            movies = movies.filter(genres__name__icontains=genre)
            any_filter_applied = True

        # Filter by actor's first name and last name
        if actor_first_name:
            movies = movies.filter(starring__first_name__icontains=actor_first_name)
            any_filter_applied = True
        if actor_last_name:
            movies = movies.filter(starring__last_name__icontains=actor_last_name)
            any_filter_applied = True

        context = {
            "movies": movies,
            "any_filter_applied": any_filter_applied
        }

        # Check if any movies were found
        if not any_filter_applied:
            messages.info(request, "Please enter search criteria.")
            messages.info(request, "list of all movies")
        # Check if any movies were found
        if not movies.exists():
            messages.info(request, "No movies found matching the search criteria.")

        return render(request, "search_movie.html", context)

    return render(request, "search_movie.html")

def edit_movies(request, id):
    if request.method == 'POST':

        title = request.POST.get('title')
        year = request.POST.get('year')
        screenplay_id = request.POST.get('screenplay')
        screenplay = Person.objects.get(id=screenplay_id)
        director_id = request.POST.get('director')
        director = Person.objects.get(id=director_id)
        rating = request.POST.get('rating')

        # data update
        movie = Movie.objects.get(pk=id)
        movie.title = title
        movie.year = year
        movie.screenplay = screenplay
        movie.director = director
        movie.rating = float(rating)
        movie.save()

        # Actors update
        starring_ids = request.POST.get('starring')
        starring_ids = [int(actor_id.strip()) for actor_id in starring_ids.split(',') if actor_id.strip()]
        starring_actors = Person.objects.filter(id__in=starring_ids)
        movie.starring.set(starring_actors)

        genres_names = request.POST.get('genres')
        genres_names = [genre_name.strip() for genre_name in genres_names.split(',') if genre_name.strip()]
        genres_objects = [Genre.objects.get_or_create(name=genre_name)[0] for genre_name in genres_names]
        movie.genres.set(genres_objects)

        # Generating the URL for the "movies" view using the reverse function
        movies_url = reverse('movies')
        return redirect(movies_url)

    movie = Movie.objects.get(pk=id)
    context = {
        "movie": movie
    }
    return render(request, "edit-movie1.html", context)


def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        year = request.POST.get('year')
        screenplay_id = request.POST.get('screenplay')
        screenplay = Person.objects.get(id=screenplay_id)
        director_id = request.POST.get('director')
        director = Person.objects.get(id=director_id)
        rating = request.POST.get('rating')

        movie = Movie()
        movie.title = title
        movie.year = year
        movie.screenplay = screenplay
        movie.director = director
        movie.rating = rating
        movie.save()

        # Handle actors (starring) and genres
        starring_ids = request.POST.get('starring')
        starring_ids = [int(actor_id.strip()) for actor_id in starring_ids.split(',') if actor_id.strip()]
        starring_actors = Person.objects.filter(id__in=starring_ids)
        movie.starring.set(starring_actors)

        genres_names = request.POST.get('genres')
        genres_names = [genre_name.strip() for genre_name in genres_names.split(',') if genre_name.strip()]
        genres_objects = [Genre.objects.get_or_create(name=genre_name)[0] for genre_name in genres_names]
        movie.genres.set(genres_objects)

        return redirect('/movies/')

    return render(request, "movie_add.html")

def del_movie(request, id):
    movie = Movie.objects.get(pk=id)
    if request.method == 'POST':
        movie.delete()
        messages.success(request, "Film removed!")
        return redirect('movies')

    context = {
        "movie": movie
    }
    return render(request, "del_movie.html", context)


def del_person(request, id):
    person = Person.objects.get(pk=id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, "Person removed!")
        return redirect('movies')
    context = {
        "person": person
    }
    return render(request, "del_person.html", context)


def show_person_list_template(request):
    persons = Person.objects.all()
    context = {
        "persons": persons
    }
    return render(request, "persons.html", context)


def show_person_template(request, id):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        person = Person.objects.get(pk=id)
        person.first_name = first_name
        person.last_name = last_name
        person.save()
        return redirect('/persons/')

    person = Person.objects.filter(pk=id)
    context = {
        "person": person
    }
    return render(request, "person_edit.html", context)


def add_person_template(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        person = Person()
        person.first_name = first_name
        person.last_name = last_name
        person.save()
        return redirect('/persons/')

    return render(request, "person_add.html")

