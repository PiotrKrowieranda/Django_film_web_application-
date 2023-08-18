from django.db import models

from django.db import models
from django.db.models import ForeignKey, ManyToManyField


class Person(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)


class Genre(models.Model):
    name = models.CharField(max_length=32)


class Movie(models.Model):
    title = models.CharField(max_length=128)
    director = ForeignKey(Person, on_delete=models.CASCADE,
        related_name="director")
    screenplay = ForeignKey(Person, on_delete=models.CASCADE,
        related_name="screenplay")
    starring = ManyToManyField(Person, through='PersonMovie', related_name='actor')
    year = models.IntegerField()
    rating = models.FloatField()
    genres = ManyToManyField(Genre)


class PersonMovie(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, null=True)











