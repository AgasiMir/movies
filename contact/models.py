from django.db import models

class Contact(models.Model):
    """Подписка по email"""

    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self) -> str:
        return self.email
