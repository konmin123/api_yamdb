# Generated by Django 3.2 on 2023-04-19 23:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('score', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Можно ввести число от 1 до 10'), django.core.validators.MaxValueValidator(10, 'Можно ввести число от 1 до 10')], verbose_name='Рейтинг')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название произведения')),
                ('year', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(1, 'Минимальный год : 1'), reviews.validators.validate_year], verbose_name='Год публикации')),
                ('description', models.TextField(verbose_name='Описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='reviews.category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(related_name='genre', to='reviews.Genres')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
            },
        ),
    ]