# Generated by Django 3.1.1 on 2020-09-13 11:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=None, max_length=100)),
                ('given_books_all_times_count', models.IntegerField(default=0)),
                ('given_books_at_the_moment', models.IntegerField(default=0)),
                ('books', models.ManyToManyField(related_name='books', to='book.Book')),
                ('librarians', models.ManyToManyField(related_name='librarians', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]