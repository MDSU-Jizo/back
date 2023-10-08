# Generated by Django 4.2.5 on 2023-10-08 10:09

import contract.constants
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('language', '0001_initial'),
        ('role', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('birthdate', models.DateField()),
                ('gender', models.CharField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Other')], default=1, max_length=10)),
                ('country', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('language_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='language.language')),
                ('role_id', models.ForeignKey(default=contract.constants.Constants.Roles['ROLE_USER'], on_delete=django.db.models.deletion.CASCADE, to='role.role')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
