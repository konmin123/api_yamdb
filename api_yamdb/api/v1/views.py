from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Review, Category, Genres, Title
from users.models import User
from .filters import TitleFilter
from .permissions import IsAdminOrSuperuser
from .permissions import IsAdminSuperuserUserOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    ReviewSerializer, CommentSerializer, CategorySerializer, GenreSerializer,
    TitleSerializer, TitleListSerializer
)
from .serializers import UserSerializer, JwtSerializer
from .service import send_email_confirmation


class ReviewViewSet(ModelViewSet):
    """
    Класс реализующий методы работы с отзывами.
    """
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminSuperuserUserOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """
    Класс реализующий методы работы с комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsAdminSuperuserUserOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CustomCategoryGenresViewSet(viewsets.GenericViewSet,
                                  mixins.ListModelMixin,
                                  mixins.CreateModelMixin,
                                  mixins.DestroyModelMixin):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CustomCategoryGenresViewSet):
    """
    Класс реализующий методы работы с категориями.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CustomCategoryGenresViewSet):
    """
    Класс реализующий методы работы с жанрами.
    """
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """
    Класс реализующий методы работы с произведениями.
    """
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    lookup_url_kwarg = 'title_id'

    def get_serializer_class(self):
        return (TitleListSerializer if self.request.method == 'GET'
                else TitleSerializer)


class UsersViewSet(ModelViewSet):
    """
    Работа с моделю User для администратора и для изменения личных данных.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=('get', 'patch'),
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """
        Метод для изменения личных данных пользователя.
        """
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MakeJwtTokenAPIView(APIView):
    """
    Выдача зарегистрированному пользователю JWT токена.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JwtSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.data['username'])
        confirmation_code = serializer.data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            token = str(AccessToken.for_user(user))
            return Response({'token': token}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation code': 'Некорректный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUpAPIView(APIView):
    """
    Регистрация пользователя или повторная отправка кода для получения токена.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            user = User.objects.filter(username=username, email=email)[0]
        else:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.create(username=username, email=email)

        confirmation_code = default_token_generator.make_token(user)
        send_email_confirmation(user, confirmation_code)
        return Response(
            {"username": username, "email": email}, status=status.HTTP_200_OK
        )
