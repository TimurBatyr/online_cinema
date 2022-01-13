from django.contrib import admin

from .models import Genre, Movie, Image


class ImageInLineAdmin(admin.TabularInline):
    model = Image
    fields = ('image',)
    max_num = 10


@admin.register(Movie)
class RecipeAdmin(admin.ModelAdmin):
    inlines =[
        ImageInLineAdmin,
    ]

admin.site.register(Genre)

