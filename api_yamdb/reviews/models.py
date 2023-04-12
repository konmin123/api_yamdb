# from .models import Title
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
# from .models import User


# отзывы на произведения
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
        verbose_name='Пользователь_автор',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=(
            MinValueValidator(1, 'Допустимое значение от 1 до 10'),
           # Raises a ValidationError with a code of 'min_value' if value is less than limit_value, which may be a callable.
           # class MinValueValidator(limit_value, message=None)[source]¶

            MaxValueValidator(10, 'Допустимое значение от 1 до 10'),
            # Raises a ValidationError with a code of 'max_value' if value is greater than limit_value, which may be a callable.
            # class MaxValueValidator(limit_value, message=None)[source]¶
        ),
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        # Создает уникальное ограничение в базе данных:
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_review',
            ),
        )

# комментарии к отзывам
class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзывы_пользователей',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст_отзыва',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)
