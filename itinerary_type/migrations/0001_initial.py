# Generated by Django 4.2.5 on 2023-10-08 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('type', '0001_initial'),
        ('itinerary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItineraryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itinerary.itinerary')),
                ('type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='type.type')),
            ],
            options={
                'db_table': 'itinerary_type',
            },
        ),
    ]
