# Generated by Django 4.2.5 on 2023-11-01 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_activate', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'db_table': 'favorite',
            },
        ),
    ]
