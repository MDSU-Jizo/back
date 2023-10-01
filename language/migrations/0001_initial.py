# Generated by Django 4.2.5 on 2023-09-30 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('isActive', models.BooleanField(blank=True, default=True, null=True)),
            ],
        ),
    ]
