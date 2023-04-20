import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genres, Title, Review, Comment
from users.models import User

from api_yamdb import settings

CSV_FILES = {
    'category': Category,
    'genre': Genres,
    'titles': Title,
    'users': User,
    'genre_title': Title.genre.through,
    'review': Review,
    'comments': Comment
}

CONTENT_DIR = settings.BASE_DIR / 'static/data'


class Command(BaseCommand):
    """
    Импортирует данные для конкретных моделей из .csv файлов.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Удаляет существующие данные конкретной Модели',
        )

    def handle(self, *args, **options):
        for file, model in CSV_FILES.items():
            with open(CONTENT_DIR / f'{file}.csv', newline='') as f:
                reader = csv.DictReader(f)
                if options["delete_existing"]:
                    model.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'Удалены старые записи {file.capitalize()}.'))
                for row in reader:
                    model.objects.create(**row)
                self.stdout.write(self.style.SUCCESS(f'Записи {file.capitalize()} созданы.'))

        self.stdout.write(self.style.SUCCESS('Поздравляем! Ваша БД наполнена!. '))
