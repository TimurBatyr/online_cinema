# Generated by Django 4.0.1 on 2022-01-12 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('slug', models.SlugField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('descriptions', models.TextField(blank=True)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.IntegerField()),
                ('country', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('producer', models.CharField(max_length=50)),
                ('age_limit', models.CharField(max_length=20)),
                ('image', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='movie.genre')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='movie.movie')),
            ],
        ),
    ]
