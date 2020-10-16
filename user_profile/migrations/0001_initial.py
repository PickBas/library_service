# Generated by Django 3.1.1 on 2020-10-16 10:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_librarian', models.BooleanField(default=False)),
                ('is_student', models.BooleanField(default=False)),
                ('base_image', models.ImageField(default='avatars/0.jpg', upload_to='avatars/')),
                ('image', models.ImageField(default='avatars/0.jpg', upload_to='avatars/')),
                ('birth', models.DateField(null=True)),
                ('books_in_use', models.ManyToManyField(related_name='books_in_use', to='book.Book')),
                ('given_books_all_times', models.ManyToManyField(related_name='given_books', to='book.Book')),
                ('overdue_books', models.ManyToManyField(related_name='overdue_books', to='book.Book')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
