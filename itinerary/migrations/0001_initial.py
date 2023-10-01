# Generated by Django 4.2.5 on 2023-09-30 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('level', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('startLocation', models.CharField(max_length=255)),
                ('endLocation', models.CharField(blank=True, max_length=255, null=True)),
                ('startDate', models.DateField()),
                ('endDate', models.DateField()),
                ('steps', models.JSONField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True)),
                ('updatedAt', models.DateTimeField(auto_now=True, null=True)),
                ('level_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='level.level')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
        ),
    ]
