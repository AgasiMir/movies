from django.db import models


class Category(models.Model):
    """Категория"""
    name = models.CharField('Категория', max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=150)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name
