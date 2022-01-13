from rest_framework import serializers

from .models import Genre, Movie, Image


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('slug',)

