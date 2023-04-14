from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from .models import Comment, Review
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Username указан неверно!')
        return data


class JwtSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)


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
