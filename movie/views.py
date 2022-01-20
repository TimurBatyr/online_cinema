from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import SearchFilter

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly


from .models import Genre, Movie, Image, Review, Likes, Rating, Favorites
from .serializers import GenreSerializer, MovieSerializer, ImageSerializer, ReviewSerializer, LikesSerializer, \
    RatingSerializer, FavoritesSerializer
from .permissions import IsAuthorPermission, PermissionMixin


# class MyPaginationClass(PageNumberPagination):
#     page_size = 4
#
#     def get_paginated_response(self, data):
#         for i in range(self.page_size):
#             text = data[i]['description']
#             data[i]['description'] = text[:20] + '...'
#         return super().get_paginated_response(data)


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['genre', ]


#CRUD
class MovieViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer



#CRUD
class MovieImagesViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorPermission]


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Likes.objects.all()
    serializer_class = LikesSerializer
    permission_classes = [IsAuthorPermission]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthorPermission]


class FavoritesCreateView(generics.CreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = self.request.user
        queryset = Favorites.objects.filter(owner=qs, favorites=True)
        return queryset


class FavoritesListView(generics.ListAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FavoriteDetailView(generics.RetrieveDestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]





