# Generated by Django 4.0.1 on 2022-01-18 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0023_alter_favorites_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='favorites',
            field=models.BooleanField(default=True),
        ),
    ]
