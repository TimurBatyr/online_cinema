# Generated by Django 4.0.1 on 2022-01-17 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0005_rename_product_review_movie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='text',
            new_name='review',
        ),
    ]
