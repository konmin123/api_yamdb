from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Status(models.TextChoices):
        USER = 'user', 'пользователь'
        MODERATOR = 'moderator', 'модератор'
        ADMIN = 'admin', 'администратор'

    email = models.EmailField(
        'Электронная почта',
        unique=True,
        max_length=254
    )
    role = models.CharField(
        'Статус пользователя',
        max_length=9,
        choices=Status.choices,
        default=Status.USER
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
