from cProfile import label
from django import forms
from django_recaptcha.fields import ReCaptchaField

from .models import Contact


class ContactForm(forms.ModelForm):
    """Форма подписки по email"""

    recaptcha = ReCaptchaField(label='')

    class Meta:
        model = Contact
        fields = ["email"]
        widgets = {
            "email": forms.TextInput(
                attrs={"class": "editContent", "placeholder": "Ваш E-mail..."}
            )
        }

        labels = {
            "email": ''
        }
