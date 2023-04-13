import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

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


class Genres(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=100
    )
    year = models.PositiveSmallIntegerField(
        'Год публикации',
        null=False,
        blank=True,
        db_index=True,
        validators=(
            MinValueValidator(1, 'min'),
            MaxValueValidator(2023, 'max')
        ),
    )
    description = models.TextField(
        'Описание',
    )
    rating = models.PositiveSmallIntegerField(
        'Рейтинг',
        blank=True,
        db_index=True,
        validators=(
            MinValueValidator(1, 'Минимальное значение: 0'),
            MaxValueValidator(10, 'Максимальное значение: 10')
        ),
    )
    genre = models.ManyToManyField(
        Genres,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='title'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
