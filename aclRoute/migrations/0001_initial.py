# Generated by Django 4.2.5 on 2023-10-31 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AclRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('is_activate', models.BooleanField(blank=True, default=True, null=True)),
            ],
            options={
                'db_table': 'aclroute',
            },
        ),
    ]
