from django.urls import path

from . import views


urlpatterns = [
    path('', views.MoviesView.as_view(), name='home'),
    path('<slug:slug>/', views.MoviesDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name='add_review'),
    path('categories/<slug:slug>/', views.CategoryView.as_view(), name='categories'),
    path('actor/<slug:slug>/', views.ActorView.as_view(), name='actor'),
]
