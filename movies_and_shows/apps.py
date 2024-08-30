from django.apps import AppConfig


class MoviesAndShowsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_and_shows'

    verbose_name = 'Фильмы и сериалы'
