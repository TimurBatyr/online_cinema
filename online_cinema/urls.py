"""online_cinema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from movie.views import GenreListView, MovieListView, MovieViewSet, MovieImagesViewSet, ReviewViewSet, LikesViewSet, \
    RatingViewSet, FavoriteDetailView, FavoritesCreateView, FavoritesListView

schema_view = get_schema_view(
    openapi.Info(
        title='Online_Cinema API',
        description='Cinema',
        default_version='v1'
    ),
    public=True,
    # permission_classes=(permissions.AllowAny, )
)

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('images', MovieImagesViewSet)
router.register('reviews', ReviewViewSet)
router.register('likes', LikesViewSet)
router.register('rating', RatingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', schema_view.with_ui('swagger')),
    path('api/v1/genres/', GenreListView.as_view()),
    path('api/v1/movie/', MovieListView.as_view()),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/', include(router.urls)),
    path('api/v1/favorites/', FavoritesListView.as_view()),
    path('api/v1/favorites/create/', FavoritesCreateView.as_view()),
    path('api/v1/favorites/<int:pk>/', FavoriteDetailView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
