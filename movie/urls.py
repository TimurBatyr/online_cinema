from django.urls import path
from . import views

urlpatterns = [
    path('genre/', views.GenreListCreateView.as_view()),
    path('genre/<int:pk>/', views.GenreDetailView.as_view()),


]