from django.db import models

# Create your models here.


class Movies(models.Model):
    movieID = models.IntegerField()
    title = models.CharField(max_length=100, blank=False)
    genres = models.CharField(max_length=250, blank=False)


class MovieUser(Movies):
    pass


class Configuration(Movies):
    pass


class UserRankingMovie(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.IntegerField()



