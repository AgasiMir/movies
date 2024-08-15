from django.db.models import Count
from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from movies.models import Actor, Category, Movie
from .forms import ReviewForm


class MixinView:
    template_name = "movies/movie_list.html"
    context_object_name = "movie_list"

    def get_mixin_context(self, context):
        context["category"] = Category.objects.annotate(
            total=Count("movie__id")
        ).filter(total__gte=1)
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


class ActorView(MixinView, DetailView): #Здесь и в MoviesDetailView я указал атрибут
    """Страница артиста"""              #template_name так как оба этих класса наследуются
    model = Actor                       #MixinView, в которм указан template_name для категорий
    template_name = "movies/actor.html" #и MoviesView. Здесь же нам нужно template_name
    context_object_name = "actor"       #переопределить
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


# class AddReview(CreateView):
#     """Отзывы"""

#     form_class = ReviewForm

#     def form_valid(self, form):
#         review = form.save(commit=False)
#         review.movie_id = self.kwargs.get("pk")
#         review.save()

#         return redirect(review.movie.get_absolute_url())
