import csv

from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genres, Title, Review, Comment
from users.models import User


CSV_PATH = 'static/data/'

FOREIGN_KEY_FIELDS = ('category', 'author')

DICT = {
    User: 'users.csv',
    Genres: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def csv_serializer(csv_data, model):
    objs = []
    for row in csv_data:
        for field in FOREIGN_KEY_FIELDS:
            if field in row:
                row[f'{field}_id'] = row[field]
                del row[field]
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'Load data from csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-existing',
            action='store_true',
            dest='delete_existing',
            default=False,
            help='Удаляет существующие данные конкретной Модели',
        )

    def handle(self, *args, **kwargs):
        for model in DICT:
            try:
                with open(CSV_PATH + DICT[model],
                          newline='',
                          encoding='utf8') as csv_file:

                    if kwargs["delete_existing"]:
                        model.objects.all().delete()
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'Записи {DICT[model][:-4]} удалены.'))

                    csv_serializer(csv.DictReader(csv_file), model)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Записи {DICT[model]} созданы.'))

            except Exception as error:
                CommandError(error)