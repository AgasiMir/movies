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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    prepopulated_fields = {"url": ("name",)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ["ava", "name"]
    list_display_links = ["ava", "name"]
    list_per_page = 5

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
    list_display = ['image', 'title', 'category']
    list_display_links = ['image', 'title']
    prepopulated_fields = {"url": ("title",)}

    # raw_id_fields = ["actors"]

    @admin.display(description='постер')
    def image(self, movie: Movie):
        if movie.poster:
            return mark_safe(f"<img src={movie.poster.url} width=120>")
        return 'Нет постера'


admin.site.register(Reviews)
admin.site.register(MovieShots)
admin.site.register(RatingStar)
admin.site.register(Rating)
