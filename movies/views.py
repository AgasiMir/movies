from django.db.models import Q, Count
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from movies.models import Actor, Category, Genre, Movie
from .forms import ReviewForm


class MixinView:
    template_name = "movies/movie_list.html"
    context_object_name = "movie_list"

    def get_mixin_context(self, context):
        context["category"] = (
            Category.objects.annotate(total=Count("movie__id"))
            .filter(total__gte=1)
        )
        # context['category'] = Category.objects.raw('''
        #                                             SELECT DISTINCT movies_category.id,
        #                                                     movies_category.name
        #                                             FROM movies_movie JOIN movies_category
        #                                             ON movies_movie.category_id =
        #                                             movies_category.id
        #                                         ''')
        context["genres"] = Genre.objects.all()
        context['get_year'] = Movie.objects.filter(draft=False).values('year')
        return context


class MoviesView(MixinView, ListView):
    """Список фильмов"""

    queryset = Movie.objects.filter(draft=False)
    extra_context = {"title": "Главная"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)


class MoviesDetailView(MixinView, DetailView):
    """Полное описание фильмов"""

    model = Movie
    context_object_name = "movie"
    template_name = "movies/movie_detail.html"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["movie"].title
        # context['title'] = self.object.title
        # context['title'] = Movie.objects.get(url=self.kwargs['url']).title
        return self.get_mixin_context(context)


class CategoryView(MixinView, ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["movie_list"][0].category.name
        return self.get_mixin_context(context)

    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs["slug"], draft=False)


class ActorView(MixinView, DetailView):
    """Страница артиста"""

    model = Actor
    template_name = "movies/actor.html"
    context_object_name = "actor"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["actor"].name
        return self.get_mixin_context(context)


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie_id = pk
            form.save()
        # return redirect(self.request.META.get('HTTP_REFERER'))
        return redirect(form.movie.get_absolute_url())


class FilterMoviesView(MixinView, ListView):
    """Фильтр Фильмов"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = ''.join([f"Год: {i} " for i in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f"Жанр: {i} " for i in self.request.GET.getlist('genre')])
        context['title'] = f"{context['year']} {context['genre']}"
        return self.get_mixin_context(context)

    def get_queryset(self):
        my_q = Q()

        if 'year' in self.request.GET:
            my_q = Q(year__in=self.request.GET.getlist('year'))
        if 'genre' in self.request.GET:
            my_q &= Q(genres__name__in=self.request.GET.getlist('genre'))

        return Movie.objects.filter(my_q)


class JsonFilterMoviesView(ListView):
    """Фильтр Фильмов JSON"""


    def get_queryset(self):
        my_q = Q()

        if 'year' in self.request.GET:
            my_q = Q(year__in=self.request.GET.getlist('year'))
        if 'genre' in self.request.GET:
            my_q &= Q(genres__name__in=self.request.GET.getlist('genre'))

        queryset =  Movie.objects.filter(my_q
        ).distinct().values('title', 'tagline', 'url', 'poster')
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)
