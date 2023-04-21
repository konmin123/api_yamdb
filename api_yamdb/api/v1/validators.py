from rest_framework import serializers

from users.models import User


def validate_me(data):
    """
    Проверка, что username не равно 'me'.
    """
    if data.get('username') == 'me':
        raise serializers.ValidationError('Username указан неверно!')
    return data


def validate_username_unique(data):
    """
    Проверка, что username уникально.
    """
    username = data.get('username')
    email = data.get('email')
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if user.email != email:
            raise serializers.ValidationError('Не уникальное имя!')
    return data


def validate_email_unique(data):
    """
    Проверка, что email уникален.
    """
    username = data.get('username')
    email = data.get('email')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        if user.username != username:
            raise serializers.ValidationError('Не уникальный email!')
    return data
