# Generated by Django 3.2 on 2023-04-16 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=256, unique=True, verbose_name='Электронная почта'),
        ),
    ]
