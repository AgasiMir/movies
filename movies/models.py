from datetime import date
from django.db import models


today = date.today()


class Category(models.Model):
    """Категория"""

    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    """Актеры и Режисеры"""

    name = models.CharField("Имя", max_length=100)
    dob = models.DateField("Дата Рождения")
    description = models.TextField("Описание")
    image = models.ImageField(upload_to="actors/%Y/%m/%d", verbose_name="Изображение")

    class Meta:
        verbose_name = "Актеры и Режисеры"
        verbose_name_plural = "Актеры и Режисеры"

    def __str__(self) -> str:
        return self.name

    def age(self):
        return (
            today.year
            - self.dob.year
            - ((today.month, today.day) < (self.dob.month, self.dob.day))
        )


class Genre(models.Model):
    """Жанры"""

    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=250, unique=True)

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    """Фильм"""

    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default="")
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/%Y/%m/%d")
    year = models.PositiveSmallIntegerField("Дата Выхода", default=2019)
    country = models.CharField("Страна", max_length=50)
    directors = models.ManyToManyField(
        Actor, verbose_name="режиссер", related_name="film_director"
    )
    actors = models.ManyToManyField(
        Actor, verbose_name="актеры", related_name="film_actor"
    )
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Премьера в мире", default=today)
    budget = models.PositiveIntegerField(
        "Бюджет", default=0, help_text="указать сумму в долларах"
    )
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указать сумму в долларах"
    )
    fees_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=250, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title

    def proper_budget(self):
        return f"{self.budget:_}".replace("_", " ")

    def proper_fees_in_usa(self):
        return f"{self.fees_in_usa:_}".replace("_", " ")

    def proper_fees_in_world(self):
        return f"{self.fees_in_world:_}".replace("_", " ")


class MovieShots(models.Model):
    """Кадры из Фильма"""

    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField(
        upload_to="movie_shots/%Y/%m/%d", verbose_name="Кадры из фильма"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    class Meta:
        verbose_name = "Кадр из Фильма"
        verbose_name_plural = "Кадры из Фильма"

    def __str__(self) -> str:
        return self.title


class RatingStar(models.Model):
    """Звезда Рейтинга"""

    value = models.PositiveSmallIntegerField("Значение", default=0)

    class Meta:
        verbose_name = "Звезда Рейтинга"
        verbose_name_plural = "Звезды Рейтинга"

    def __str__(self) -> str:
        return self.value


class Rating(models.Model):
    """Рейтинг"""

    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name="звезда"
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self) -> str:
        return f"{self.star} - {self.movie}"


class Reviews(models.Model):
    """Отзывы"""

    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        "self",
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self) -> str:
        return f"{self.name} - {self.movie}"
