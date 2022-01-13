
from django.shortcuts import render
from rest_framework import generics, permissions
from django_filters import rest_framework as filters

from movie import serializers
from movie.models import Genre, Movie


class GenreListCreateView(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer



