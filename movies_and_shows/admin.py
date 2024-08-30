from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Video, Season

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['poster', 'title', 'movie', 'season']
    list_display_links = ['poster', 'title']

    @admin.display(description='Изображение')
    def poster(self, video: Video):
        if video.movie.poster:
            return mark_safe(f"<img src={video.movie.poster.url} width=80>")
        return 'Нет постера'


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['movie', 'season']
