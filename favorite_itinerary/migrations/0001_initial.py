# Generated by Django 4.2.5 on 2023-11-01 18:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('favorite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteItinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='favorite.favorite')),
            ],
            options={
                'db_table': 'favorite_itinerary',
            },
        ),
    ]
