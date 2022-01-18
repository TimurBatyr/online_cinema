from rest_framework import serializers

from .models import Genre, Movie, Image, Review, Likes


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
        # movie = self.context.get('movie')
        # validated_data['user'] = owner
        # validated_data['product'] = movie
        # return super().create(validated_data)


# class FavoriteSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Favorite
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['owner'] = instance.user.email
#         representation['movie'] = instance.movie.title
#         return representation

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
