from rest_framework import serializers

from .models import Genre, Movie, Image


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', )


class MovieSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
        # exclude = ('owner', )

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     images_data = request.FILES
    #     author = request.user
    #     movie = Movie.objects.create(author=author, **validated_data)
    #     for image in images_data.getlist('images'):
    #         Image.objects.create(image=image, movie=movie)
    #     return movie
    #
    # def update(self, instance, validated_data):
    #     request = self.context.get('request')
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     images_data = request.FILES
    #     instance.images.all().delete()
    #     for image in images_data.getlist('images'):
    #         Image.objects.create(image=image, movie=instance)
    #     return instance
    #
    def to_representation(self, instance):
        representation = super().to_representation(instance)
    #     representation['author'] = instance.owner.email
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
    #     representation['comments'] = CommentSerializer(instance.comments.all(), many=True).data
    #     representation['likes'] = instance.likes.all().count()
    #     representation['rating'] = instance.rating.aggregate(Avg('rating'))
        return representation


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
        # exclude = ['movie', ]

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        return representation
