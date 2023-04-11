from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import mixins, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (UserSerializer, JwtSerializer,
                             UsersForAdminSerializer, PersonalUserSerializer)
from api.permissions import IsAdmin, IsPersonalOnly
from api.service import send_email_confirmation, check_user_in_base
from api.models import User


class UsersForAdminViewSet(ModelViewSet):
    """Работа с пользователями для администратора"""
    queryset = User.objects.all()
    serializer_class = UsersForAdminSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )


class PersonalUserViewSet(GenericViewSet, mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin):
    """Работа с пользователями для администратора"""
    queryset = User.objects.all()
    serializer_class = PersonalUserSerializer
    permission_classes = [IsPersonalOnly]


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
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)}, status=status.HTTP_200_OK
                )
            return Response({
                'confirmation code': 'Некорректный код подтверждения!'},
                status=status.HTTP_400_BAD_REQUEST)


class SignUpAPIView(APIView):
    """Выдача зарегистрированному пользователю JWT токена"""
    permission_classes = [AllowAny]

    def post(self, request):
        if check_user_in_base(request):
            send_email_confirmation(username=request.data['username'])
            return Response({
                "username": request.data['username'],
                "email": request.data['email']},
                status=status.HTTP_200_OK)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.data['username']
            email = serializer.data['email']
            User.objects.get_or_create(username=username, email=email)
            send_email_confirmation(username=username)
            return Response({
                "username": username, "email": email},
                status=status.HTTP_200_OK)

