# Generated by Django 4.0.1 on 2022-01-17 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_movie_link_to_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='link_to_movie',
            field=models.URLField(blank=True),
        ),
    ]
