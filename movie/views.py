from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Genre, Movie, Image
from .serializers import GenreSerializer, MovieSerializer, ImageSerializer


class GenreListView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['genre', ]


#CRUD
class MovieViewSet(viewsets.ModelViewSet): #PermissionMixin,
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # queryset_any = Favorite.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request, pk=None):             # /search/?q=xxx
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


#CRUD
class MovieImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    # def get_serializer_context(self):
    #     return {'request': self.request}
