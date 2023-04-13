from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True,
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
        default=True)  # сомнение есть по булеву значению

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
            'title'
        )
        validators = (
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
            ),
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
