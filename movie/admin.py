from django.contrib import admin

from .models import Genre, Movie, Image, Review


class ImageInLine(admin.TabularInline):
    model = Image
    max_num = 5
    min_num = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ]


admin.site.register(Genre)
admin.site.register(Review)


