# Generated by Django 4.2.5 on 2023-10-28 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itinerary', '0001_initial'),
        ('favorite_itinerary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoriteitinerary',
            name='itinerary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itinerary.itinerary'),
        ),
    ]
