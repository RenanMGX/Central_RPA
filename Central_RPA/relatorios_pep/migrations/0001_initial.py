# Generated by Django 5.1 on 2025-02-21 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('argv', models.TextField()),
                ('value', models.TextField()),
            ],
        ),
    ]
