import datetime

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
    confirmation_code = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


def current_year():
    return datetime.date.today().year


class Title(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField(
        'Дата публикации',
        null=False,
        blank=True,
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='title'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title_id = models.ForeignKey(
        Title,
        related_name='title_id',
        blank=True,
        null=False,
        on_delete=models.CASCADE,
    )
    genre_id = models.ForeignKey(
        Genres,
        related_name='genre_id',
        blank=True,
        null=False,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('title_id', 'genre_id',),
                name='unique_genre',
            ),
        )

    def __str__(self):
        return f'Жанр произведения: {self.title_id} - {self.genre_id}'

