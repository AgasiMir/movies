from django.shortcuts import redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from movies.models import Movie
from .forms import ReviewForm


class MoviesView(ListView):
    """Список фильмов"""

    queryset = Movie.objects.filter(draft=False)
    context_object_name = "movie_list"
    extra_context = {"title": "Главная"}


class MoviesDetailView(DetailView):
    """Полное описание фильмов"""

    model = Movie
    context_object_name = "movie"
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = context["movie"].title
        # context['title'] = self.object.title
        # context['title'] = Movie.objects.get(url=self.kwargs['url']).title
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
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
