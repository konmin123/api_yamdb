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
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=256
    )
    year = models.PositiveSmallIntegerField(
        'Год публикации',
        null=False,
        blank=True,
        db_index=True,
        validators=(
            MinValueValidator(1, 'Минимальный год : 1'),
            MaxValueValidator(2023, 'Максимальный год: 2023')
        ),
    )
    description = models.TextField(
        'Описание',
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='genre'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='category'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=(
            MinValueValidator(1, 'Можно ввести число от 1 до 10'),
            MaxValueValidator(10, 'Можно ввести число от 1 до 10'),
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review',
            ),
        )

    def __str__(self):
        return f'произведение {self.pk}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Комментарий к отзыву',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
