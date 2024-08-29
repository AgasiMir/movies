from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserLoginForm, UserRegisterForm


class UserLoginView(LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    extra_context = {"title": "Авторизация"}
    next_page = "/"


class UserRegisterView(CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    extra_context = {"title": "Регистрация"}

    def get_success_url(self) -> str:
        return reverse_lazy('users:login')


class UserLogoutView(LogoutView):
    next_page = "/"
