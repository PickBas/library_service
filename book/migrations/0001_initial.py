# Generated by Django 3.1.1 on 2020-09-13 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('since_given', models.DateTimeField(default=django.utils.timezone.now)),
                ('since_back', models.DateTimeField(default=django.utils.timezone.now)),
                ('in_use_by', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='current_book_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]