from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status, filters
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg

from .filters import TitleFilter
from .models import Review, Category, Genres, Title, User
from .service import send_email_confirmation, check_user_in_base
from .permissions import (
    IsAdminSuperuserUserOrReadOnly, IsAdminOrReadOnly, IsAdminOrSuperuser
)
from .serializers import (
    ReviewSerializer, CommentSerializer, CategorySerializer, GenreSerializer,
    TitleSerializer, TitleListSerializer, UserSerializer, JwtSerializer
)


class UsersViewSet(ModelViewSet):
    """Работа с моделю User для администратора и для изменения личных данных"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperuser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Метод для изменения личных данных пользователя"""
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
    """Выдача зарегистрированному пользователю JWT токена"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JwtSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.data['username']
            )
            if user.confirmation_code == serializer.data['confirmation_code']:
                token = str(AccessToken.for_user(user))
                return Response({'token': token}, status=status.HTTP_200_OK)
            return Response(
                {'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )


class SignUpAPIView(APIView):
    """Выдача зарегистрированному пользователю JWT токена"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if check_user_in_base(request):
            pass
        elif serializer.is_valid(raise_exception=True):
            User.objects.create(username=username, email=email)
        send_email_confirmation(username=username)
        return Response(
            {"username": username, "email": email}, status=status.HTTP_200_OK
        )


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminSuperuserUserOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminSuperuserUserOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleListSerializer
        return TitleSerializer
