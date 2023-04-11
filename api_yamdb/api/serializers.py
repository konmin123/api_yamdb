from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UsersForAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class PersonalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class JwtSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(max_length=200, required=True)
