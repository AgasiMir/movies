from django.db.models import Q, Count
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from movies.models import Actor, Category, Genre, Movie, Rating
from .forms import ReviewForm, RatingForm


class MixinView:
    template_name = "movies/movie_list.html"
    context_object_name = "movie_list"

    def get_template_names(self):
        if "big" in self.request.GET:
            return ["movies/movie_list.html"]
        if 'small' in self.request.GET:
            return ["movies/movie_list_2.html"]
        return super().get_template_names()

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
    extra_context = {"title": "Фильмы и Сериалы"}
    paginate_by = 9

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
        context['star_form'] = RatingForm()
        return self.get_mixin_context(context)


class CategoryView(MixinView, ListView):
    """Категории"""

    paginate_by = 9

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

    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = ''.join([f"year={i}&" for i in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f"genre={i}&" for i in self.request.GET.getlist('genre')])
        context['title'] = 'Жанры и Года'
        return self.get_mixin_context(context)

    def get_queryset(self):
        my_q = Q()

        if 'year' in self.request.GET:
            my_q = Q(year__in=self.request.GET.getlist('year'))
        if 'genre' in self.request.GET:
            my_q &= Q(genres__name__in=self.request.GET.getlist('genre'))

        return Movie.objects.filter(my_q).distinct()


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


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(data=request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get('movie')),
                defaults={'star_id': int(request.POST.get('star'))}
            )
            return HttpResponse(status=201)
        return HttpResponse(status=400)


class Search(MixinView, ListView):
    """Поиск фильмов"""

    paginate_by = 9
    search_obj = None

    def get_queryset(self):
        if 'q' in self.request.GET:
            self.__class__.search_obj = self.request.GET.get('q').capitalize()
        return Movie.objects.filter(title__icontains=self.__class__.search_obj)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context)
