from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserLoginForm(AuthenticationForm):
    """Форма логина"""

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class UserRegisterForm(UserCreationForm):
    """Форма регистрации"""

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]
