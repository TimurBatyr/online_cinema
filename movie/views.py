from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Genre, Movie, Image, Review
from .serializers import GenreSerializer, MovieSerializer, ImageSerializer, ReviewSerializer
from .permissions import IsAuthorPermission


# class MyPaginationClass(PageNumberPagination):
#     page_size = 4
#
#     def get_paginated_response(self, data):
#         for i in range(self.page_size):
#             text = data[i]['description']
#             data[i]['description'] = text[:20] + '...'
#         return super().get_paginated_response(data)


class PermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', ]:
            permissions = [IsAdminUser, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]


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


    # def get_serializer_context(self):
    #     return {'request': self.request}


    # @action(detail=False, methods=['get'], permission_classes=[AllowAny, ])
    # def search(self, request, pk=None):             # /search/?q=xxx
    #     q = request.query_params.get('q')
    #     queryset = self.get_queryset()
    #     queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
    #     serializer = MovieSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)


#CRUD
class MovieImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # def get_serializer_context(self):
    #     return {'request': self.request}


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorPermission]

    # def get_serializer_context(self):
    #     return {'request': self.request}


# class UpdateDeleteReview(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthorPermission]
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)