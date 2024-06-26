# Generated by Django 3.2.25 on 2024-03-30 12:45

import NewsApp.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[NewsApp.models.validate_author_name_length])),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=64)),
                ('category', models.CharField(choices=[('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology'), ('trivia', 'Trivia')], max_length=10)),
                ('region', models.CharField(choices=[('uk', 'UK'), ('eu', 'European'), ('w', 'World')], max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('details', models.CharField(max_length=128)),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='NewsApp.author')),
            ],
        ),
    ]
