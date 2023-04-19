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
from .service import check_user_in_base, send_email_confirmation


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
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenresViewSet(CustomCategoryGenresViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    lookup_url_kwarg = 'title_id'

    def get_serializer_class(self):
        return (TitleListSerializer if self.request.method == 'GET'
                else TitleSerializer)


class SignUpAPIView(APIView):
    """
    Создает нового пользователя, если email и username
    уникальны, и отправляет письмо с подтверждением
    на указанный email.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        if check_user_in_base(request):
            pass
        elif serializer.is_valid(raise_exception=True):
            User.objects.get_or_create(username=username, email=email)
        send_email_confirmation(username=username)
        return Response(
            {"username": username, "email": email}, status=status.HTTP_200_OK
        )


class UsersViewSet(ModelViewSet):
    """Работа с моделю User для администратора и для изменения личных данных"""
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
    """API view для создания JWT токена."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = JwtSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                User, username=serializer.validated_data['username']
            )
            token = serializer.validated_data['confirmation_code']
            if default_token_generator.check_token(user, token):
                access_token = str(AccessToken.for_user(user))
                return Response({'token': access_token}, status=status.HTTP_200_OK)
            return Response(
                {'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST
            )

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def make_jwt_token_api_view(request):
#     """
#     API view для создания JWT токена.
#     POST запрос ожидает данные в формате, указанном в JwtSerializer.
#     """
#
#     if request.method == 'POST':
#         serializer = JwtSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user = get_object_or_404(
#                 User, username=serializer.validated_data['username']
#             )
#             token = serializer.validated_data['confirmation_code']
#             if default_token_generator.check_token(user, token):
#                 access_token = str(AccessToken.for_user(user))
#                 return Response({'token': access_token}, status=status.HTTP_200_OK)
#             return Response(
#                 {'confirmation code': 'Некорректный код подтверждения!'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )