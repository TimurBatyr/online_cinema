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


RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class Review(models.Model):
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.review)

    class Meta:
        ordering = ('-created_at',)


# class Favorite(models.Model):
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favourites')
#     owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favourites')
#     favorite = models.BooleanField(default=True)

class Likes(models.Model):
    likes = models.BooleanField(default=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes')
    owner = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return str(self.likes)