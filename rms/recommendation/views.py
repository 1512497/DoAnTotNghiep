from django.shortcuts import render
from .models import *


# Create your views here.

# return page


def index(request):
    return render(request, 'index.html')


def display_movies(request):
    items = Movies.objects.all()
    context = {
        'items': items
    }
    return render(request, 'index.html', context)


def user_ranking_movie(requets):
    items = UserRankingMovie.objects.all()
    context = {
        'items': items
    }
    return render(requets, 'ranking.html', context)


