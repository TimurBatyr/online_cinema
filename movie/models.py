from django.db import models

from account.models import MyUser


class Genre(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.name)


class Movie(models.Model):
    owner = models.ForeignKey(MyUser, related_name='movies', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies')
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.PositiveIntegerField()
    link_to_movie = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
