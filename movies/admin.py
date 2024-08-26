from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Actor,
    Genre,
    Movie,
    MovieShots,
    RatingStar,
    Rating,
    Reviews,
)


class ReviewsInLine(admin.TabularInline):
    model = Reviews
    extra = 0
    readonly_fields = ["name", "text", "email", "parent", "movie"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"url": ("name",)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ["ava", "name"]
    list_display_links = ["ava", "name"]
    list_per_page = 10

    exclude = ["url"]
    readonly_fields = ["ava"]

    @admin.display(description="фото")
    def ava(self, actor: Actor):
        if actor.image:
            return mark_safe(f"<img src={actor.image.url} width=120>")
        return "Нет фото"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"url": ("name",)}


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ["category", "year", "genres"]
    list_display = ["image", "title", "category", "comments"]
    list_display_links = ["image", "title"]
    list_per_page = 5

    save_on_top = True
    save_as = True
    # raw_id_fields = ["actors"]
    prepopulated_fields = {"url": ("title",)}
    inlines = [ReviewsInLine]

    @admin.display(description="постер")
    def image(self, movie: Movie):
        if movie.poster:
            return mark_safe(f"<img src={movie.poster.url} width=120>")
        return "Нет постера"

    @admin.display(description='комментарии')
    def comments(self, movie:Movie):
        if movie.reviews_set.count() > 0:
            return movie.reviews_set.count()
        return 'Комментариев пока нет'

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):

    readonly_fields = ["name", "text", "email", "parent", "movie"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['film_poster', 'movie', 'star', 'ip']
    list_display_links = ['film_poster', 'movie']
    list_per_page = 5

    readonly_fields = ['movie', 'star', 'ip', 'film_poster']


    @admin.display(description='Изображение')
    def film_poster(self, rating: Rating):
        if rating.movie.poster:
            return mark_safe(f"<img src={rating.movie.poster.url} width=80>")
        return 'Нет фото'

admin.site.register(MovieShots)
admin.site.register(RatingStar)



admin.site.site_title = 'Фильмы и Сериалы'
admin.site.site_header = 'Фильмы и Сериалы'
