from django.db.models import Avg
from rest_framework import serializers

from .models import Genre, Movie, Image, Review, Likes, Rating, Favorites


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # representation['owner'] = instance.owner.email
        representation['images'] = ImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['likes'] = instance.likes.all().count()
        representation['rating'] = instance.rating.aggregate(Avg('rating'))
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


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        # context это {}, из вьюшки передаем в сериалайзер
        request = self.context.get('request')
        owner = request.user
        review = Review.objects.create(owner=owner, **validated_data)
        return review




class LikesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Likes
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        owner = request.user
        movie = validated_data.get('movie')
        like = Likes.objects.get_or_create(owner=owner, movie=movie)[0]
        like.likes = True if like.likes is False else False
        like.save()
        return like


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        owner = request.user
        movie = validated_data.get('movie')
        rating = Rating.objects.get_or_create(owner=owner, movie=movie)[0]
        rating.rating = validated_data['rating']
        rating.save()
        return rating


class FavoritesSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Favorites
        fields = ('id', 'movie', 'favorites', 'owner',)

