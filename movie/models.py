from django.db import models


class Genre(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.slug


class Movie(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movie')
    title = models.CharField(max_length=150)
    descriptions = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    quantity = models.IntegerField()
    country = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    producer = models.CharField(max_length=50)
    age_limit = models.CharField(max_length=20)
    image = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='images')
