from django.template import Library

from movies.models import Movie

register = Library()


@register.inclusion_tag("movies/recent.html")
def recent():
    recent_movies = Movie.objects.all().order_by("-id")[:5]
    return {"recent_movies": recent_movies}
