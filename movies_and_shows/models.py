from django.db import models

from movies.models import Movie


class Season(models.Model):
    season = models.PositiveSmallIntegerField("Сезон", default=1)
    movie = models.ForeignKey(
        Movie, verbose_name="Сериал", on_delete=models.CASCADE, related_name="season"
    )

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"

    def __str__(self) -> str:
        return f"{self.movie} - {self.season}"


class Video(models.Model):
    """Видео файлы"""

    title = models.CharField("Загаловок", max_length=250)
    description = models.TextField("Описание", blank=True)
    video = models.FileField("Видео", upload_to="Video/%Y/%m/%d")
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)
    season = models.ForeignKey(
        Season,
        verbose_name="Сериал",
        on_delete=models.CASCADE,
        related_name="episode",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Видео Файл"
        verbose_name_plural = "Видео Файлы"

    def __str__(self) -> str:
        return self.title
