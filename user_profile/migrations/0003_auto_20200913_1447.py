# Generated by Django 3.1.1 on 2020-09-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
        ('user_profile', '0002_auto_20200913_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='books_in_use',
            field=models.ManyToManyField(related_name='books_in_use', to='book.Book'),
        ),
        migrations.AddField(
            model_name='profile',
            name='given_books_all_times',
            field=models.ManyToManyField(related_name='given_books', to='book.Book'),
        ),
    ]