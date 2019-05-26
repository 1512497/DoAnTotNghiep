from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^display_movies$', display_movies, name='display_movies'),
    url(r'^user_ranking_movie$', user_ranking_movie, name='user_ranking_movie')
]